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
            "level": 3
        }, {
            "_id": 0,
            "name": 1,
            "cat_id": 1
        }))


class GoodDetail(BaseModel):
    collection_name = 'good_detail'

    def get(self, id):
        return self.collection.find_one(filter={'_id': id})


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
