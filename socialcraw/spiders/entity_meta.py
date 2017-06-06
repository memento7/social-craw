# -*- coding: utf-8 -*-
import scrapy
import json
import requests

from socialcraw import security
from socialcraw import items
from socialcraw.utils import cprint


class EntityMetaSpider(scrapy.Spider):
	name = "entity-meta"


	def start_requests(self) :
		# Get entities from API Server

		user_entities = []
		page_num = 0
		while True :
			r = requests.get(
				url='https://api.memento.live/publish/entities?page=%d' % page_num,
				headers={
					'Authorization': security.API_AUTH,
					'Content-Type': 'application/json',
				},
			)

			data = json.loads(r.text)

			if type(data) is not list or len(data) == 0 : break

			user_entities += data
			page_num += 1

		
		for entity in user_entities:
			search_key = entity['nickname']
			subkey = entity.get('subkey', None)

			if subkey :
				search_key = subkey + " " + search_key

			yield scrapy.Request(
				url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%s' % search_key,
				callback=self.parse_naver,
				meta={'entity': entity},
			)



	def parse_naver(self, response) :
		""" Parse Instagram username and profile image on NAVER
		"""
		entity = response.meta.get('entity')
		entity_id = entity['id']

		detail_profile = response.css('.profile_wrap .detail_profile').extract_first()
		
		member_thumb_url = response.css('.profile_wrap .member_thumb img').xpath('@src').extract_first()
		profile_image_url = response.css('.profile_wrap .big_thumb img').xpath('@src').extract_first()

		if not profile_image_url and member_thumb_url :
			profile_image_url = member_thumb_url

		if profile_image_url :
			profile_image_exists = False

			for image in entity['images'] :
				if image['type'] == 'profile' :
					profile_image_exists = True
					break

			if not profile_image_exists :
				yield items.ProfileImageItem(
					entity_id=entity_id,
					image_link=profile_image_url,
				)


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




