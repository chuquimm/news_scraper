# Spider to testing

import scrapy

class TestingSpider(scrapy.Spider):
    name = 'testing'
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        #'MEMUSAGE_NOTIFY_MAIL': ['SOME@EMAIL.COM'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'NEWSSRAPER',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

            next_page = response.xpath(
                '//ul[@class="pager"]//li[@class="next"]/a/@href').get()
            if next_page:
                # add relative url
                yield response.follow(next_page, callback=self.parse_quotes, cb_kwargs={'quotes': quotes})
            else:
                yield {'quotes': quotes}

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        # scrapy crawl testing -a top=1
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            tags = tags[:top]

        yield {
            'title': title,
            'tags': tags,
        }

        next_page = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page:
            # add relative url
            yield response.follow(next_page, callback=self.parse_quotes, cb_kwargs={'quotes': quotes})
