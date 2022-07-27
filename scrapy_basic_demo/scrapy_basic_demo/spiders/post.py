import scrapy


class PostSpider(scrapy.Spider):
    name = 'post'
    allowed_domains = ['baidu.com']
    start_urls = ['https://fanyi.baidu.com/sug']  # 百度翻译 POST 请求接口

    def start_requests(self):  # 重写父类方法，函数必须返回可迭代对象
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata={'kw': 'baby'}, callback=self.parse)

    def parse(self, response):
        print(response.json())  # 获取JSON响应
