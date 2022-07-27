import scrapy


class GetSpider(scrapy.Spider):
    name = 'get'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
