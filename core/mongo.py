from pymongo import MongoClient
from django.conf import settings

# Підключення до локального інстансу MongoDB
# Формат URL: mongodb://username:password@host:port/
MONGO_URI = "mongodb://root:rootpassword@localhost:27017/"

client = MongoClient(MONGO_URI)

# Назва нашої бази даних (якщо її немає, Mongo створить її автоматично при першому записі)
db = client['asset_metadata_db']

# Наша колекція для метаданих файлів
metadata_collection = db['asset_metadata']