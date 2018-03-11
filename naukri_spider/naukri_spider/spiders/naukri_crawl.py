# -*- coding: utf-8 -*-
import scrapy
import re
from time import sleep
import random
import csv
from naukri_spider.spiders.query_process import process_query

class NaukriCrawlSpider(scrapy.Spider):
    name = 'naukri_crawl'
    allowed_domains = ['www.naukri.com/']
    #start_urls = ['http://www.naukri.com//']

    def start_requests(self):
                
        filename = r"E:\pdftotext\xml_data.csv"
        file = open(filename, encoding = 'ISO-8859-1')
        reader = csv.reader(file)
        self.COUNT_MAX = 4
        num_rows = 0
        for rows in reader:
            query = rows[2]
            num_rows += 1
            if len(query)!=0 and query!= 'empty' and num_rows>=580:
                self.url = 'https://www.naukri.com/' + process_query(query) + '-jobs'
                #print(url)
                self.count = 0
                yield scrapy.Request(url=self.url, callback=self.parse)
                

        #urls = ['https://www.naukri.com/bigdata-jobs']
        #for url in urls:
        #    self.count = 0
        #    yield scrapy.Request(url=url, callback=self.parse)

    ''' 
    Parse is a call back method and is predefined in scrapy.Spider class.
    And if we change the name parse to something else it will give an error.
    XPath handles any XML or HTML document as a tree.
    '''
    
    def parse(self, response):

        self.count = self.count + 1
        all_titles = response.xpath('//*[re:match(@id, "[0-9]+")]/a/ul/li').extract()
        comp1 = re.compile(r'(title=".*?")')
        all_skills = response.xpath('//*[re:match(@id, "[0-9]+")]/a/div/div/span').extract()
        comp2 = re.compile(r'(>.*\s*\n*?<)')

        for i in range(0, len(all_skills)):
            title_group = comp1.search(all_titles[i])
            title = title_group.group()

            skills_group = comp2.search(all_skills[i])
            skills = skills_group.group()

            yield {'URL': self.url, 'Title': title, 'Skills': skills}

        sleep(random.randrange(1, 8))
        
        new_url = response.xpath('//*[@class="pagination"]/a/@href').extract_first()
        #print(new_url)
        #print(self.count)

        if (new_url is not None) and (self.count <= self.COUNT_MAX):
            yield scrapy.Request(url = new_url, callback = self.parse, dont_filter = True) 