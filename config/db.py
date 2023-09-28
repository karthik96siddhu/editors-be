from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# configuration Mongo Connection
cluster = MongoClient(os.getenv('MONGO_URL'))
db = cluster[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]
admin_collection = db[os.getenv('ADMIN_COLLECTION_NAME')]