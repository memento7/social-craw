# -*- coding: utf-8 -*-
import scrapy
import json

from socialcraw import security

class InstaFollowersSpider(scrapy.Spider):
	name = "insta-followers"

	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch, br',
		'Accept-Language': 'ko,en;q=0.8,en-US;q=0.6,da;q=0.4,la;q=0.2',
		'Cache-Control': 'max-age=0',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	}


	def start_requests(self):
		ids = ['taehee35', 'kimsejeong101']
		#ids = ['0soo.2', 'kimsejeong101']

		for id in ids:
			url = 'https://www.instagram.com/%s/' % id
			yield scrapy.Request(url=url, headers=InstaFollowersSpider.headers, callback=self.parse_id)


	def parse_id(self, response):
		
		shared_data = response.text.split('<script type="text/javascript">window._sharedData = ')[1].split(';</script>')[0]
		shared_data = json.loads(shared_data)

		id = shared_data['entry_data']['ProfilePage'][0]['user']['id']
		url = 'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id=%s&first=20' % id
		#url = 'https://lab.prev.kr/h.php?query_id=17874545323001329&id=%s&first=20' % id

		yield scrapy.Request(url=url, headers=InstaFollowersSpider.headers, cookies=security.cookies, callback=self.parse_followers)



	def parse_followers(self, response):
		
		yield json.loads(response.text)



