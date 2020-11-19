# Spider to testing

import scrapy

class TestingSpider(scrapy.Spider):
    name = 'testing'
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
    }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall() # top 10

        yield {
            'title': title,
            'quotes': quotes,
            'tags': tags,
        }

        next_page = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse) # add relative url
