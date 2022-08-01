# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    top_category_name = scrapy.Field()
    top_category_url = scrapy.Field()
    sub_category_name = scrapy.Field()
    sub_category_url = scrapy.Field()

    url = scrapy.Field()
    name = scrapy.Field()
    author_name = scrapy.Field()
    price = scrapy.Field()


