import scrapy
from ..items import DangdangItem
from scrapy_redis.spiders import RedisSpider


class BookRedisSpider(RedisSpider):
    name = 'book_redis'
    # allowed_domains = ['dangdang.com']
    # start_urls = ['https://category.dangdang.com/']

    redis_key = 'book_redis:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(BookRedisSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 获取所有图书顶级分类节点列表
        top_node_list = response.xpath('//div[@class="classify_left"]/div[1]/div[@class="classify_kind"]')

        for top_node in top_node_list:
            top_category_name = top_node.xpath('./div[@class="classify_kind_name"]/a/text()').get()
            top_category_url = response.urljoin(top_node.xpath('./div[@class="classify_kind_name"]/a/@href').get())

            # print(top_category_name, top_category_url)

            # 获取所有图书子级分类节点列表(排除更多链接干扰)
            sub_node_list = top_node_list.xpath('./ul[@class="classify_kind_detail"]/li'
                                                '/a[not (@href="javascript:void(0);")]')

            for sub_node in sub_node_list:
                sub_category_name = sub_node.xpath('./text()').get()
                sub_category_url = response.urljoin(sub_node.xpath('./@href').get())

                meta = dict(
                    top_category_name=top_category_name,
                    top_category_url=top_category_url,
                    sub_category_name=sub_category_name,
                    sub_category_url=sub_category_url
                )

                # print('PARSE: ', sub_category_url)
                yield scrapy.Request(
                    url=sub_category_url,
                    callback=self.parse_book_list,
                    meta=meta
                )

    def parse_book_list(self, response):
        print('PARSE_BOOK_LIST: ', response.url)
        # # 图书列表页面所有图书列表
        # book_node_list = response.xpath('//div[@id="search_nature_rg"]/ul[@class="bigimg"]/li')
        # for book in book_node_list:
        #     item = DangdangItem()
        #
        #     item['top_category_name'] = response.meta['top_category_name']
        #     item['top_category_url'] = response.meta['top_category_url']
        #     item['sub_category_name'] = response.meta['sub_category_name']
        #     item['sub_category_url'] = response.meta['sub_category_url']
        #
        #     item['url'] = response.urljoin(book.xpath('./p[@class="name"]/a/@href').get())
        #     item['name'] = book.xpath('./p[@class="name"]/a/text()').get().strip()
        #     item['author_name'] = ','.join(
        #         book.xpath('./p[@class="search_book_author"]/span/a[@name="itemlist-author"]/text()').getall()
        #     )
        #     item['price'] = book.xpath('./p[@class="price"]/span/text()').get()
        #
        #     yield item
