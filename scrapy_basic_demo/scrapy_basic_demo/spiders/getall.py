import scrapy


class DushuSpider(scrapy.Spider):
    name = 'getall'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/1617.html']

    def parse(self, response):
        title_list = response.xpath('//div[@class="bookslist"]//h3/a/@title')
        # 使用 `getall()` 方法获取 Selector 对象内容
        print(title_list.getall())
