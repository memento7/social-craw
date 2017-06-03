# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProfileImageItem(scrapy.Item):
	entity_id = scrapy.Field()
	image_link = scrapy.Field()


class InstaUserInfoItem(scrapy.Item):
	entity_id = scrapy.Field()
	insta_id = scrapy.Field()
	username = scrapy.Field()
	data = scrapy.Field()


class InstaUserFollowsItem(scrapy.Item):
	entity_id = scrapy.Field()
	follows = scrapy.Field()
