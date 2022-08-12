import scrapy


class DownloadImagesSpider(scrapy.Spider):
    name = 'download_images'
    allowed_domains = ['umei.cc']
    start_urls = ['http://umei.cc/']

    def parse(self, response):
        pass
