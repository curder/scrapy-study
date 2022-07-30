import scrapy
from ..items import DushuSpiderItem

class DushuSpider(scrapy.Spider):
    name = 'getall'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/1617.html']

    def parse(self, response):
        book_info_nodes = response.xpath('//div[@class="book-info"]')

        for info_node in book_info_nodes:
            title = info_node.xpath('.//h3/a/@title').get()
            author = info_node.xpath('.//p/text()').get()

            # 以可迭代的形式返回给引擎
            # 使用yield语句返回可迭代对象
            yield DushuSpiderItem(title=title, author=author)
            # yield {"title": title, "author": author}
            # yield dict(title=title, author=author)
