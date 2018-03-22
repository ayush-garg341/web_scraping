# -*- coding: utf-8 -*-
import scrapy
import csv
import re
from time import sleep
import random

class StateCityCrawlSpider(scrapy.Spider):
    name = 'state_city_crawl'
    allowed_domains = ['ratekhoj.com']
    #start_urls = ['www.ratekhoj.com/']

    def start_requests(self):
    	self.new_url = 'http://www.ratekhoj.com/' + 'atm/atmlocations.php?searchstring=State+Bank+Of+India&page=1'
    	yield scrapy.Request(url=self.new_url, callback=self.parse)


    def parse(self, response):
    	x = response.xpath('//*[re:match(@class,"(odd|even)")]/td//text()').extract()
    	city = []
    	state = []
    	for i in range(0, len(x)):
    		if x[i]=='City:':
    			city.append(x[i+1].lower().strip())

    		if x[i]=='State:':
    			state.append(x[i+1].lower().strip())

    	for c, s in zip(city, state):
    		yield { 'State':s, 'City':c }

    	sleep(random.randrange(1, 8))

    	updated_url = response.xpath('//center/big/a[contains(., "Next")]/@href').extract_first()
    	if updated_url is not None:
    		updated_url = 'http://www.ratekhoj.com/' + updated_url
    		yield scrapy.Request(url = updated_url, callback = self.parse, dont_filter = True)
