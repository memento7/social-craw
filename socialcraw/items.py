# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaUserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    entity_id = scrapy.Field()
    insta_id = scrapy.Field()
    username = scrapy.Field()
    data = scrapy.Field()


class InstaUserFollowsItem(scrapy.Item):
    # define the fields for your item here like:
    entity_id = scrapy.Field()
    follows = scrapy.Field()
