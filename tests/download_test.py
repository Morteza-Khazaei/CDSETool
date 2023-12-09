from cdsetool.query import query_features
from cdsetool.download import download_feature

from cdsetool.credentials import Credentials

username = r'mortezakhazaei1370@gmail.com'
password = r'Morteza@1370'
credentials = Credentials(username, password)
print(credentials)



s2_tiles = ['39STD', '39STC', '39STB', '38SQJ', '38SQH', 
             '38SQG', '39SUC', '39SUB', '39SUA', '39SWA', 
             '39SWV', '39SVB', '39SVA', '39SXA', '39SXV', 
             '39SYB', '39SYA', '39SYV', '40SBG', '40SBF', 
             '40SCH', '40SCG', '40SCF', '40SDH', '40SDG']

# from datetime import date

# date_from = date(2023, 7, 1)
# date_to = date(2023, 8, 1)



# for tile_id in s2_tiles:
#     product_query = {
#         'tileId': tile_id, 
#         'startDate': date_from, 
#         'completionDate': date_to,
#         'productType': 'S2MSI1C',
#         'cloudCover': '[0,10]'
#     }
#     features = query_features('Sentinel2', product_query)
    
#     for feature in features:
#         print(feature)
#         download_feature(feature, 'E:/ssiec-co/DATASETS/', {'credentials': credentials})
        
#     #     break
#     # break
