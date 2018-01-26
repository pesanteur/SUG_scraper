# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy.item import Field


class SugScraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Date = Field()
    #Location = Field()
    Time = Field()
    Status = Field()
    DES_Group = Field()
