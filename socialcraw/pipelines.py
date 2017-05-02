# -*- coding: utf-8 -*-

from socialcraw import items
from socialcraw import spiders
from socialcraw.utils import cprint


class InstaIdPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_id.InstaIdSpider :
			return item


		# TODO: API CALL

		cprint.ok( item )
		return item


class InstaFollowsPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_follows.InstaFollowsSpider :
			return item

		cprint.warn( item.get('entity_id') )
		cprint.warn( item.get('follows') )

		# TODO: API CALL

		return item

