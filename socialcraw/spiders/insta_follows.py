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
		ids = ['taehee35', 'kimsejeong101']

		for id in ids:
			yield scrapy.Request(
				url='https://www.instagram.com/%s/?__a=1' % id,
				cookies=security.insta_cookies,
				callback=self.parse_user,
				meta={'id': id},
			)


	def parse_user(self, response) :
		entity_id = response.meta.get('entity_id')
		data = json.loads(response.text)['user']
		insta_id = data['id']

		user = items.InstaUserInfoItem(
			entity_id=entity_id,
			insta_id=insta_id,
			username=data['username'],
			data=data,
		)
		yield user

		yield scrapy.Request(
			url='https://www.instagram.com/graphql/query/?query_id=17874545323001329&id=%s&first=200' % id,
			cookies=security.insta_cookies,
			callback=self.parse_followers,
			meta={'user': user},
		)



	def parse_followers(self, response) :
		user = response.meta.get('user')
		
		data = json.loads(response.text)
		follows = data['data']['user']['edge_follow']['edges']

		yield items.InstaUserFollowsItem(
			user=user,
			follows=follows,
		)



