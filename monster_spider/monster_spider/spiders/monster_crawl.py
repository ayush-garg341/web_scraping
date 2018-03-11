# -*- coding: utf-8 -*-
import scrapy
from time import sleep
import csv
import random


class MonsterCrawlSpider(scrapy.Spider):
    name = 'monster_crawl'
    allowed_domains = ['monsterindia.com']
    #start_urls = ['http://monsterindia.com/']

    def start_requests(self):
    	
    	filename = r"C:\pythoncode\scrapy-crawler\job_titles.csv"
    	file = open(filename, encoding = 'ISO-8859-1')
    	reader = csv.reader(file)
    	self.COUNT_MAX = 200
    	num_rows = 0
    	for rows in reader:
    		self.query = rows[0]
    		num_rows += 1
    		if num_rows > 1:
    			processed_query = '-'.join(self.query.lower().split(' '))
    			self.url = 'http://www.monsterindia.com/' + processed_query + '-jobs.html'
    			self.count = 0
    			self.url_count = 1
    			yield scrapy.Request(url=self.url, callback=self.parse)


    	'''
    	urls = ['http://www.monsterindia.com/data-analyst-jobs.html']
    	for url in urls:
    		yield scrapy.Request(url=url, callback=self.parse)
		'''

    def parse(self, response):
    	jobs = response.xpath('//a[@class="title_in"]/@href').extract()
    	for job in jobs:
    		self.count += 1
    		if self.count <= self.COUNT_MAX:
    			yield scrapy.Request(url=job, callback=self.parse_jobs)
   
    	sleep(random.randrange(1, 8))
    	new_url = response.xpath('//a[contains(text(), "Next")]/@althref').extract_first()
    	if new_url is not None:
    		self.url_count += 1
    		new_made_url = self.url[:-5] + '-' + str(self.url_count) + '.html'
    		yield scrapy.Request(url = new_made_url, callback = self.parse, dont_filter = True) 

    def parse_jobs(self, response):
    	jds = response.xpath('//div[@class="job_description "]/descendant::text()').extract()
    	company = response.xpath('//a[@class="company"]/text()').extract_first()
    	key_skills = response.xpath('//h2[@class="keyskill skillseotag"]/descendant::text()').extract()
    	skills = ' '.join(key_skills)
    	jd = ' '
    	prev = jd[-1]
    	for line in jds:
    		jd = jd + ' '
    		for char in line:
    			if ord(char)<=127:
    				if (char == '\n' or char == '\t' or char == ' ') and prev == ' ':
    					continue

    				elif (char == '\n' or char == '\t') and prev != ' ':
    					jd = jd + ' '
    					prev = jd[-1]
    				
    				else:
    					jd = jd + char
    					prev = jd[-1]

    	yield {'TITLE':self.query, 'COMAPNY NAME':company, 'SKILL SET': skills, 'JOB DESCRIPTION': jd.strip()}
