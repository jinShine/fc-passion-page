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

        # instagram_collection.remove({})

        # insta_datas = insta_fetch_feed()
        # for data in insta_datas:
        
        #     instagram_collection.insert_one({
        #         'id': data['id'],
        #         'image_url': data['image_url'],
        #         'insta_url': data['insta_url'],
        #         'post_type': data['post_type']
        #     })

        return instagram_collection.find({}, {'_id': False}).sort('id', -1)





    