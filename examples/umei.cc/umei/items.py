# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UmeiItem(scrapy.Item):
    id = scrapy.Field()  # 详情ID
    path = scrapy.Field()  # 文件存储路径
    image_url = scrapy.Field()  # 存储图片URL
    images = scrapy.Field()  #
