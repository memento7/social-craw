# -*- coding: utf-8 -*-
import scrapy
import json

from socialcraw import security
from socialcraw import items


class InstaFollowsSpider(scrapy.Spider):
	""" TO BE FIXED
	"""
	name = "insta-follows"

	def start_requests(self) :
		# user_entities: temp data
		user_entities = [
			{
				'id': 1,
				'sns': {
					'instagram': '1474623111'
				}
			},
			{
				'id': 2,
			},
			{
				'id': 3,
			},
			{
				'id': 4,
			},
			{
				'id': 5,
				'sns': {
					'instagram': '3408064405'
				}
			},
			{
				'id': 6,
			},
		]

		for entity in user_entities:
			if 'sns' not in entity : continue

			insta_id = entity['sns']['instagram']

			yield scrapy.Request(
				url='https://www.instagram.com/graphql/query/?query_id=17874545323001329&id=%s&first=200' % insta_id,
				cookies=security.insta_cookies,
				callback=self.parse_followers,
				meta={'entity': entity},
			)



	def parse_followers(self, response) :
		""" Get follows by instagram id
		"""
		entity = response.meta.get('entity')
		
		data = json.loads(response.text)
		edges = data['data']['user']['edge_follow']['edges']

		follows = []
		for node in edges :
			follows.append( node['node']['id'] )

		yield items.InstaUserFollowsItem(
			entity_id=entity['id'],
			follows=follows,
		)



