# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # amazome Item
    url = scrapy.Field()
    productID = scrapy.Field()
    one = scrapy.Field()
    two = scrapy.Field()
    three = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    initCartUrl = scrapy.Field()
    shopID = scrapy.Field()
