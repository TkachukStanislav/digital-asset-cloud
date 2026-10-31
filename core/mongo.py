from pymongo import MongoClient

client = MongoClient('mongodb://root:rootpassword@localhost:27017/')
db = client['digital_asset_cloud']

# Used by core/views.py
metadata_collection = db['asset_metadata']

# Used by core/tasks.py
def get_asset_metadata_collection():
    return metadata_collection