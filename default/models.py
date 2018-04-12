import pymongo
from base.settings import MONGO_URI, MONGO_DB
# Create your models here.


class BaseModel(object):
    collection_name = None

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        if self.collection_name is None:
            raise NotImplementedError
        else:
            self.collection = self.db[self.collection_name]

    def __del__(self):
        self.client.close()


class Category(BaseModel):
    collection_name = 'category'

    def get_category_three(self):
        return list(self.collection.find({
            "is_list": True,
            "level": 3,
            "cat_id": {"$ne": None}
        }, {
            "_id": 0,
            "name": 1,
            "cat_id": 1
        }).sort("hot", pymongo.DESCENDING).limit(50))

    def inc_hot(self, cat_id):
        return self.collection.update({
            "cat_id": cat_id
        }, {"$inc": {"hot": 1}}
        )

    def search(self, q):
        return list(self.collection.find({
            "$text": {
                "$search": q
            },
            "is_list": True,
            "level": 3
        }, {
            "_id": 0,
            "name": 1,
            "path": 1,
            "url": 1,
            "cat_id": 1
        }).limit(10))


class GoodDetail(BaseModel):
    collection_name = 'good_detail'

    def get(self, _id):
        return self.collection.find_one(filter={'_id': _id})


class GoodList(BaseModel):
    collection_name = 'good_list'

    def get(self, _id):
        return self.collection.find_one(filter={'_id': _id})


class BaseANalysisResult(BaseModel):

    def is_done(self, _id):
        old_analysis_result = self.collection.find_one({"_id": _id})
        return old_analysis_result if old_analysis_result else None

    def save(self, document):
        return self.collection.save(document)


class GoodListAnalysisResult(BaseANalysisResult):
    collection_name = 'good_list_analsis_result'


class GoodDetailAnalysisResult(BaseANalysisResult):
    collection_name = 'good_detail_analsis_result'

    def inc_hot(self, _id):
        return self.collection.update({
            "_id": _id
        }, {"$inc": {"hot": 1}}
        )

    def get_top_ana(self):
        return list(self.collection.find({}, {
            "_id": 1,
            "name": 1
        }).sort("hot", pymongo.DESCENDING).limit(8))


class SpiderTask(BaseModel):
    collection_name = "spider_task"

    def save(self, document: dict):
        return self.collection.save(document)

    def get(self, _id):
        return self.collection.find_one(filter={"_id": _id})

    def delete(self, _id):
        return self.collection.delete_one({"_id": _id})
