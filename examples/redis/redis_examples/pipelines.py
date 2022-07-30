# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime


class ScrapyRedisExamplePipeline:
    def process_item(self, item, spider):
        item["crawled"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["spider"] = spider.name
        return item
