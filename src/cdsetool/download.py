"""
Download features from a Copernicus Data Space Ecosystem OpenSearch API result

Provides a function to download a single feature, and a function to download
all features in a result set.
"""
import os
import random
import tempfile
import json
import time
from cdsetool._processing import _concurrent_process
from cdsetool.credentials import Credentials
from cdsetool.monitor import NoopMonitor



def get_value_from_json(json_object, key):
    try:
        data = json.loads(json_object)
        keys = key.split('.')
        value = data

        for k in keys:
            value = value[k]

        return value
    except (json.JSONDecodeError, KeyError):
        return None


def download_feature(feature, path, options=None):
    """
    Download a single feature

    Returns the feature ID
    """
    options = options or {}
    url = _finditem(feature, 'url')
    filename = _finditem(feature, 'title')
    iid = _finditem(feature, 'id')

    if not url or not filename:
        return iid

    # if os.path.exists(file):
    #     return feature.get("id")

    fpath = os.path.join(path, filename.replace(".SAFE", ".zip"))
    if not os.path.exists(fpath):
        with _get_monitor(options).status() as status:
            status.set_filename(filename)

            session = _get_credentials(options).get_session()
            url = _follow_redirect(url, session)
            response = _retry_backoff(url, session)

            content_length = int(response.headers["Content-Length"])

            status.set_filesize(content_length)

            fd, temp_path = tempfile.mkstemp(dir=path)  # pylint: disable=invalid-name
            with open(temp_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024 * 5):
                    if not chunk:
                        continue

                    file.write(chunk)
                    status.add_progress(len(chunk))

            os.close(fd)
            # Download successful, rename the temporary file to its proper name
            os.rename(temp_path, fpath)
            # shutil.move(temp_path, path)

    return iid


def download_features(features, path, options=None):
    """
    Generator function that downloads all features in a result set

    Feature IDs are yielded as they are downloaded
    """
    options = options or {}

    options["credentials"] = _get_credentials(options)

    options["monitor"] = _get_monitor(options)
    options["monitor"].start()

    def _download_feature(feature):
        return download_feature(feature, path, options)

    for feature in _concurrent_process(
        _download_feature, features, options.get("concurrency", 1)
    ):
        yield feature

    options["monitor"].stop()


def _finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem(v, key)
            if item is not None:
                return item


def _get_feature_url(feature):
    return feature.get("properties").get("services").get("download").get("url")


def _follow_redirect(url, session):
    response = session.head(url, allow_redirects=False)
    while response.status_code in range(300, 400):
        url = response.headers["Location"]
        response = session.head(url, allow_redirects=False)

    return url


def _retry_backoff(url, session):
    response = session.get(url, stream=True)
    while response.status_code != 200:
        time.sleep(60 * (1 + (random.random() / 4)))
        response = session.get(url, stream=True)

    return response


def _get_monitor(options):
    return options.get("monitor") or NoopMonitor()


def _get_credentials(options):
    return options.get("credentials") or Credentials()
