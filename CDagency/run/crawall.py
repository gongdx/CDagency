from scrapy import cmdline
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from pymongo import MongoClient

import time

while True:
    
    #运行所有爬虫
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['sample']

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider :
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()

    #分数据库
    client = MongoClient('localhost', 27017)
    db = client['CDagency']
    unified_col = db['unified'].find()

    for item in unified_col:
        coll_name = item['col_name']
        db[coll_name].update({'title': item['title']}, {'$set': dict(item)}, True, True)
    
    #间隔时间
    time.sleep(604800) #间隔一周