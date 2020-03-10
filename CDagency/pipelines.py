# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawer):
        return cls(
            mongo_uri=crawer.settings.get('MONGO_URI'),
            mongo_db=crawer.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # self.db[CDshangwujuItem.collection].create_index([('pub_time', pymongo.ASCENDING)])
        # self.db[CDguanglvju.collection].create_index([('pub_time', pymongo.ASCENDING)])

    def process_item(self, item, spider):
        # name = item.__class__.__name__
        # self.db[name].insert(dict(item))

        #方式一：分部门存储在collection
        #col_name = item["col_name"]             #获取集合名称
        #方式二：统一存储在一个collection
        col_name = 'unified'

        self.db[col_name].update({'title': item['title']}, {'$set': dict(item)}, True, True)
                                                #根据新闻标题进行去重，无重复则创建新字段
        return item

    def close_spider(self, spider):
        self.client.close()
