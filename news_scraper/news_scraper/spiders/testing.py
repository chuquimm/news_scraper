# Spider to testing

import scrapy

class TestingSpider(scrapy.Spider):
    name = 'testing'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        print('*' * 10)
        print('\n\n')
        print(response.status, response.headers)
        print('\n\n')
        print('*' * 10)
