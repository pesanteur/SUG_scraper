# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo import IndexModel, ASCENDING
from items import SugScraperItem

class SugScraperPipeline(object):
    def __init__(self):
	client = pymong.MongoClient("localhost", 27017)
	db = client["SUG_scraper"]
	self.SUGscrape = db["SUGscrape"]
	index = IndexModel([('link_url', ASCENDING)], unique=True)
	self.SUGscrape.create_indexes([index])

    def process_item(self, item, spider):
	print('MongoDBItem', item)
	if isinstance(item, SugScraperItem):
	  print('SugScraper Item True')
        try:
              self.SUGscrape.update_one({'link_url': item['link_url']}, {'$set': dict(item)}, upsert=True)
        except Exception:
            pass
        return item
