# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    day = scrapy.Field()  # 日期
    aqi = scrapy.Field()  # AQI
    quality_level = scrapy.Field()  # 质量等级
    pm_2_5 = scrapy.Field()  # PM2.5
    pm_10 = scrapy.Field()  # PM10
    co = scrapy.Field()  # CO
    so2 = scrapy.Field()  # SO2
    no2 = scrapy.Field()  # NO2
    o3_8h = scrapy.Field()  # O3_8h
