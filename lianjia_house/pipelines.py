# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class LianjiaHousePipeline(object):

    def __init__(self):
        mongo_host = 'localhost'
        mongo_port = 27017
        mongo_database = 'test'
        mongo_collection = 'lianjia_house'

        client = pymongo.MongoClient(mongo_host, mongo_port)

        db = client[mongo_database]

        self.collection = db.get_collection(mongo_collection)


    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
