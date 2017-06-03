# -*- coding: utf-8 -*-
import requests

from socialcraw import security
from socialcraw import items
from socialcraw import spiders
from socialcraw.utils import cprint

API_BASE = 'https://manage.memento.live/api'

class ProfileImagePipeline(object):
	def process_item(self, item, spider):
		if type(item) != items.ProfileImageItem :
			return item

		cprint.ok( item )

		# Register profile image
		r = requests.post(
			url=API_BASE+'/persist/entities/%s/images' % item.get('entity_id'),
			json=[{
				'source_link': item.get('image_link'),
				'url': item.get('image_link'),
				'weight': 0,
				'type': 'profile',
			}],
			headers={
				'Authorization': security.API_AUTH,
				'Content-Type': 'application/json',
			},
		)
		r.raise_for_status()
		cprint.okb(r)

		return item



class InstaIdPipeline(object):
	def process_item(self, item, spider):
		if type(item) != items.InstaUserInfoItem :
			return item

		if item.get('insta_id') == None :
			return item

		cprint.ok( item )

		# Register instagram ID
		r = requests.post(
			url=API_BASE+'/persist/entities/%d/sns' % item.get('entity_id'),
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
			url=API_BASE+'/persist/entities/%d/relations' % item.get('entity_id'),
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

