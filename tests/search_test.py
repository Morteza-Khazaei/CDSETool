import pandas as pd
import requests



json = requests.get("http://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?startDate=2021-07-01T00:00:00Z&completionDate=2021-07-31T23:59:59Z&sortParam=startDate&maxRecords=20").json()
df = pd.DataFrame.from_dict(json['features'])
print(df.head())

# iterating the columns
for col in df.columns:
    print(df['properties'].keys())