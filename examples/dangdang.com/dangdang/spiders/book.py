import scrapy
from ..items import DangdangItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['dangdang.com']
    start_urls = ['https://category.dangdang.com/']

    def parse(self, response):
        # 获取所有图书顶级分类节点列表
        top_node_list = response.xpath('//div[@class="classify_left"]/div[1]/div[@class="classify_kind"]')

        for top_node in top_node_list[:10]:
            top_category_name = top_node.xpath('./div[@class="classify_kind_name"]/a/text()').get()
            top_category_url = response.urljoin(top_node.xpath('./div[@class="classify_kind_name"]/a/@href').get())

            # print(top_category_name, top_category_url)

            # 获取所有图书子级分类节点列表
            sub_node_list = top_node_list.xpath('./ul[@class="classify_kind_detail"]/li/a')

            for sub_node in sub_node_list[:10]:
                sub_category_name = sub_node.xpath('./text()').get()
                sub_category_url = response.urljoin(sub_node.xpath('./@href').get())

                meta = dict(
                    top_category_name=top_category_name,
                    top_category_url=top_category_url,
                    sub_category_name=sub_category_name,
                    sub_category_url=sub_category_url
                )

                yield scrapy.Request(url=sub_category_url, callback=self.parse_book_list, meta=meta)

    def parse_book_list(self, response):
        # 图书列表页面所有图书列表
        book_node_list = response.xpath('//div[@id="search_nature_rg"]/ul[@class="bigimg"]/li')
        for book in book_node_list:
            item = DangdangItem()

            item['top_category_name'] = response.meta['top_category_name']
            item['top_category_url'] = response.meta['top_category_url']
            item['sub_category_name'] = response.meta['sub_category_name']
            item['sub_category_url'] = response.meta['sub_category_url']

            item['url'] = response.urljoin(book.xpath('./p[@class="name"]/a/@href').get())
            item['name'] = book.xpath('./p[@class="name"]/a/text()').get().strip()
            item['author_name'] = ','.join(
                book.xpath('./p[@class="search_book_author"]/span/a[@name="itemlist-author"]/text()').getall()
            )
            item['price'] = book.xpath('./p[@class="price"]/span/text()').get()
            yield item
