# -*- coding: utf-8 -*-
import scrapy
import re
from time import sleep
import random
from naukri_spider.spiders.query_process import process_query

class NaukriSkillCrawlSpider(scrapy.Spider):
    name = 'naukri_skill_crawl'
    allowed_domains = ['www.naukri.com']
    #start_urls = ['http://www.naukri.com/']

    def __init__(self, skill = None, *args, **kwargs):
        super(NaukriSkillCrawlSpider, self).__init__(*args, **kwargs)
        start_url = 'https://www.naukri.com/' + process_query(skill) + '-jobs'
        self.start_urls = [start_url] 

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        all_skills = response.xpath('//*[re:match(@id, "[0-9]+")]/a/div/div/span').extract()
        comp2 = re.compile(r'(>.*\s*\n*?<)')

        for i in range(0, len(all_skills)):
            skills_group = comp2.search(all_skills[i])
            skills = skills_group.group()
            skills = skills.replace('<', '')
            skills = skills.replace('>', '')
            skills = skills.replace('...', '')

            yield {'Skills': skills}

        sleep(random.randrange(1, 8))


# scrapy crawl naukri_skill_crawl -a skill="big data"