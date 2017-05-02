# -*- coding: utf-8 -*-

from socialcraw import items
from socialcraw import spiders
from socialcraw.utils import cprint


class InstaIdPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_id.InstaIdSpider :
			return

		cprint.ok( item )
		return item


class InstaFollowsPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_follows.InstaFollowsSpider :
			return item


		if type(item) == items.InstaUserInfoItem :
			pass


		if type(item) == items.InstaUserFollowsItem :
			# Yeh!
			cprint.warn( len(item.get('follows') ) )
			cprint.warn( item.get('user').get('insta_id') )


		return item



# import json

# class JsonWriterPipeline(object):

# 	def open_spider(self, spider):
# 		self.file = open('data/tmp.jl', 'w')

# 	def close_spider(self, spider):
# 		self.file.close()

# 	def process_item(self, item, spider):
# 		line = json.dumps(dict(item)) + "\n"
# 		self.file.write(line)
# 		return item


