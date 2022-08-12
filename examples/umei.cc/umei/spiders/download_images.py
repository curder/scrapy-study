import re

import scrapy
from ..items import UmeiItem


class DownloadImagesSpider(scrapy.Spider):
    name = 'download_images'
    allowed_domains = ['umei.cc', 'shanghai-jiuxin.com']
    start_urls = ['https://www.umei.cc/meinvtupian/meinvxiezhen/']

    def parse(self, response):
        # 1. 分析目标页面图片列表，找到图片详情页
        image_detail_urls = response.xpath('//ul[contains(@class, "pic-list")]/li/a/@href').getall()
        for url in image_detail_urls[:1]:
            id = self.get_page_id(url)
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_image_detail, meta={"id": id})

    # 处理页面详情
    def parse_image_detail(self, response):
        # 1. 分析下一页图片详情和其他组图片地址
        xpath = '//div[@class="gongneng"]//a/@href|//div[@class="img-box"]/following-sibling::a/@href'
        next_page_urls = response.xpath(xpath).getall()
        for url in next_page_urls:
            id = self.get_page_id(url)
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_image_detail,
                meta={"id": id}
            )

        # 2. 分析出页面中待下载的图片地址
        response.xpath('//section[@class="img-content"]//img/@src').get()
        item = UmeiItem()
        item['id'] = response.request.meta['id']
        yield item

    def get_page_id(self, url):
        return re.compile(r'(?P<id>\d+)(_\d+)*.htm', re.S).search(url).group('id')
