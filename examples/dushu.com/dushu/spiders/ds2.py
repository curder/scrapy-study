import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Ds2Spider(CrawlSpider):
    name = 'ds2'
    allowed_domains = ['dushu.com']
    start_urls = ['https://www.dushu.com/book/1617.html']

    rules = (
        # 提取详情页链接
        Rule(LinkExtractor(allow=r'/book/\d+/'), callback='parse_item', follow=False),

        # 提取分页页码列表链接
        Rule(LinkExtractor(allow=r'/book/1617_\d+\.html'), follow=True),
    )

    def parse_item(self, response):
        id = response.url.strip('/').split('/')[-1]
        title = response.xpath('//div[@class="book-title"]/h1/text()').get()
        image_url = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@examples').get()
        price = response.xpath('//p[@class="price"]/span[@class="num"]/text()').get('0')
        author = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[1]/td[2]/text()').get('')
        publishing_house = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[2]/td[2]/text()').get()
        description = response.xpath("//div[@class='book-summary'][1]//div[@class='text txtsummary']/text()").get('')

        yield dict(
            id=id,
            title=title,
            image_url=image_url,
            price=price,
            author=author,
            publishing_house=publishing_house,
            description=description,
        )
