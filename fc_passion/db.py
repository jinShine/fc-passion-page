import config
from pymongo import MongoClient
from instagram_api import insta_fetch_feed

class DB():

    def __init__(self, client=None):
        self.client = MongoClient(config.MongoDB_URL, 27017)

    def fcpassion_db(self):
        return self.client.fcpassion

    def get_insta_api(self):
        instagram_collection = self.fcpassion_db().instagram
        return instagram_collection.find({}, {'_id': False}).sort('id', 1)