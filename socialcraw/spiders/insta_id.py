# -*- coding: utf-8 -*-
import scrapy
import json
import requests

from socialcraw import security
from socialcraw import items
from socialcraw.utils import cprint

class InstaIdSpider(scrapy.Spider):
	name = "insta-id"


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
			search_key = entity['nickname']
			subkey = entity.get('subkey', None)

			if subkey :
				search_key += " " + subkey

			yield scrapy.Request(
				url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%s' % search_key,
				callback=self.parse_username,
				meta={'entity_id': entity['id']},
			)



	def parse_username(self, response) :
		""" Parse Instagram username on NAVER
		"""
		entity_id = response.meta.get('entity_id')
		detail_profile = response.css(".detail_profile").extract_first()
		

		if (not detail_profile) or ('인스타그램' not in detail_profile) :
			# User don't have official account
			username = None

		else :
			# Parse username
			idx = detail_profile.index('인스타그램')
			tmp = detail_profile[0:idx]
			tmp = tmp[tmp.rfind('href="') + 6 : ]
			tmp = tmp[: tmp.find('"')]

			username = tmp[len('http://instagram.com/') : ]



		if not username :
			# If account not exists, yield Item with None
			yield items.InstaUserInfoItem(
				entity_id=entity_id,
				insta_id=None,
				username=None,
			)

		else :
			# If account exists, get uid
			yield scrapy.Request(
				url='https://www.instagram.com/%s/?__a=1' % username,
				cookies=security.insta_cookies,
				callback=self.parse_id,
				meta={
					'entity_id': entity_id,
					'username': username,
				},
			)



	def parse_id(self, response) :
		""" Parse Instagram id on instagram.com
		"""

		data = json.loads(response.text)['user']

		yield items.InstaUserInfoItem(
			entity_id=response.meta.get('entity_id'),
			username=response.meta.get('username'),
			insta_id=data['id'],
		)




