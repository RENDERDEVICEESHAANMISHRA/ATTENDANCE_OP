# db_operations.py

from pymongo import MongoClient
import datetime

class DBOperations:
    def __init__(self):
        # Use your MongoDB connection string
        self.client = MongoClient('mongodb+srv://cloudeshaan05:FKCfTwIDY2sPcpxl@face.4ecgw2p.mongodb.net/?retryWrites=true&w=majority&appName=FACE')
        self.db = self.client['FACE']  # Use your database name
        self.users_collection = self.db['users']
        self.log_collection = self.db['logs']

    def insert_user(self, name, embeddings):
        user_data = {
            'name': name,
            'embeddings': embeddings
        }
        result = self.users_collection.insert_one(user_data)
        return result.inserted_id

    def get_all_user_embeddings(self):
        users = self.users_collection.find()
        return list(users)

    def log_login_logout(self, name, action):
        log_data = {
            'name': name,
            'action': action,
            'timestamp': datetime.datetime.now()
        }
        result = self.log_collection.insert_one(log_data)
        return result.inserted_id
