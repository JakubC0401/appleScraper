# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import pymongo

class ScrapperPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
          'mongodb+srv://kubac04:<password>@cluster0.s4xjf.mongodb.net/test'
        )
        db = self.conn['appleProducts']
        self.collection = db['cortland']

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
