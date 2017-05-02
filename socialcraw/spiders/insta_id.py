# -*- coding: utf-8 -*-
import scrapy
import json

from socialcraw import security
from socialcraw import items
from socialcraw.utils import cprint

class InstaIdSpider(scrapy.Spider):
	name = "insta-id"


	def start_requests(self) :
		user_entities = [
			{
				'id': 1,
				'nickname': '김태희',
				'realname': '김태희',
				'subkey': '',
			},
			{
				'id': 2,
				'nickname': '비',
				'realname': '정지훈',
				'subkey': '가수',
			},
			{
				'id': 3,
				'nickname': '공유',
				'realname': '공지철',
				'subkey': '배우',
			},
			{
				'id': 4,
				'nickname': '최순실',
				'realname': '최서원',
				'subkey': '배우',
			},
			{
				'id': 5,
				'nickname': '김세정',
				'realname': '김세정',
				'subkey': '아이오아이',
			},
			{
				'id': 6,
				'nickname': '박근혜',
				'realname': '박근혜',
				'subkey': '',
			},
		]
		
		for entity in user_entities:
			search_key = entity['nickname']
			if entity['subkey'] :
				search_key += " " + entity['subkey']

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




