# -*- coding: utf-8 -*-
import requests

from socialcraw import security
from socialcraw import items
from socialcraw import spiders
from socialcraw.utils import cprint


class InstaIdPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_id.InstaIdSpider :
			return item

		if item.get('insta_id') == None :
			return item

		cprint.ok( item )


		# Register instagram ID
		r = requests.post(
			url='https://api.memento.live/persist/entities/%d/sns' % item.get('entity_id'),
			json={
				'relation_type': 'INSTAGRAM',
				'social_key': item.get('insta_id'),
			},
			headers={
				'Authorization': security.API_AUTH,
				'Content-Type': 'application/json',
			},
		)
		r.raise_for_status()
		cprint.okb(r)

		return item


class InstaFollowsPipeline(object):
	def process_item(self, item, spider):
		if type(spider) != spiders.insta_follows.InstaFollowsSpider :
			return item

		cprint.ok( item.get('entity_id') )
		cprint.ok( item.get('follows') )

		# Register instagram relation
		r = requests.post(
			url='https://api.memento.live/persist/entities/%d/relations' % item.get('entity_id'),
			json={
				'metadata': {},
				'relation_type': 'INSTAGRAM',
				'target_keys': item.get('follows')
			},
			headers={
				'Authorization': security.API_AUTH,
				'Content-Type': 'application/json',
			},
		)
		r.raise_for_status()
		cprint.okb(r)

		return item

