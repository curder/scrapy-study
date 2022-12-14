import re

import scrapy
import hashlib
from ..items import UmeiItem
from scrapy.utils.python import to_bytes
from scrapy_redis.spiders import RedisSpider


class DownloadImagesSpider(RedisSpider):
    name = 'download_images'
    # allowed_domains = ['umei.cc', 'shanghai-jiuxin.com', 'zutuanla.com']
    # start_urls = ['https://www.umei.cc/meinvtupian/meinvxiezhen/']
    redis_key = 'download_images:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(DownloadImagesSpider, self).__init__(*args, **kwargs)

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
        image_url = response.xpath('//section[@class="img-content"]//img/@src').get()
        item = UmeiItem()
        item['id'] = response.request.meta['id']

        item['image_url'] = image_url.replace('http://kr.shanghai-jiuxin.com/', 'https://kr.zutuanla.com/')

        item['path'] = f'origin/{item["id"]}-{hashlib.sha1(to_bytes(item["image_url"])).hexdigest()}.jpg'

        yield item

    def get_page_id(self, url):
        return re.compile(r'(?P<id>\d+)(_\d+)*.htm', re.S).search(url).group('id')
