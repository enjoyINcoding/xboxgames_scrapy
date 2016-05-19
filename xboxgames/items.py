# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XboxgamesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_id = scrapy.Field()
    title = scrapy.Field()
    title_zh = scrapy.Field()
    price = scrapy.Field()
    full_price = scrapy.Field()
    is_gold = scrapy.Field()
    detail_url = scrapy.Field()
    country = scrapy.Field()

    pass
