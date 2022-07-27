import scrapy


class GetSpider(scrapy.Spider):
    name = 'get'  # 爬虫的名称，用于启动爬虫程序
    allowed_domains = ['baidu.com']  # 允许的域名，限定爬虫只能爬取这个域名下的内容
    start_urls = ['http://baidu.com/']  # 起始URL，可以配置多个，当爬虫开始时，列表中的URLs将封装成球球对象提交给引擎

    def parse(self, response):  # 解析函数，用于解析爬取数据的内容，当引擎回传给Spider一个响应对象时触发回调
        print(response.url)
