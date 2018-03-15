import pymongo
from base.settings import MONGO_URI, MONGO_DB
# Create your models here.


class BaseModel(object):

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]

    def __del__(self):
        self.client.close()


class Category(BaseModel):
    collection = 'category'

    def get_category_three(self):
        return list(self.db[self.collection].find({
            "is_list": True,
            "level": 3
        }, {
            "_id": 0,
            "name": 1,
            "cat_id": 1
        }))

