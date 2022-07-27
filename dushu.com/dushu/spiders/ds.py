import scrapy


class DsSpider(scrapy.Spider):
    name = 'ds'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/1617.html']

    def parse(self, response):
        # 提取书本详情链接
        href_list = response.xpath('//div[@class="book-info"]/div/a/@href').getall()
        for href in href_list:
            detail_url = 'https://www.dushu.com' + href
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

        # 提取分页链接
        page_list = response.xpath('////div[@class="pages"]//a/@href').getall()
        for href in page_list:
            url = 'https://www.dushu.com' + href
            yield scrapy.Request(url=url, callback=self.parse)

    # 解析详情页逻辑
    def parse_detail(self, response):
        title = response.xpath('//div[@class="book-title"]/h1/text()').get()
        image_url = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@src').get()
        price = response.xpath('//p[@class="price"]/span[@class="num"]/text()').get('0')
        author = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[1]/td[2]/text()').get('')
        publishing_house = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[2]/td[2]/text()').get()
        description = response.xpath("//div[@class='book-summary'][1]//div[@class='text txtsummary']/text()").get('')

        yield dict(
            title=title,
            image_url=image_url,
            price=price,
            author=author,
            publishing_house=publishing_house,
            description=description,
        )
