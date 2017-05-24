# -*- coding: utf-8 -*-
import scrapy
import json
import requests

from socialcraw import security
from socialcraw import items


class InstaFollowsSpider(scrapy.Spider):
	name = "insta-follows"

	def start_requests(self) :
		# Get entities from API Server
		r = requests.get(
			url='https://api.memento.live/publish/entities',
			headers={
				'Authorization': security.API_AUTH,
				'Content-Type': 'application/json',
			},
		)
		user_entities = json.loads(r.text)

		for entity in user_entities:
			try :
				insta_id = entity['role_json']['PERSON']['data']['sns']['instagram']
			except e:
				continue

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



