# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class ScrapyBasicDemoPipeline:

    # 周期函数，当蜘蛛开始工作时触发
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'getall':
            self.file = open('getall.json', 'a', encoding='utf-8')

    # 周期函数，当蜘蛛结束工作时触发
    def colse_spider(self, spider):
        if spider.name == 'getall':
            self.file.close()

    def process_item(self, item, spider):
        print('PIPLINE: ', item)
        if spider.name == 'getall':
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item  # 返回给下一个管道使用
