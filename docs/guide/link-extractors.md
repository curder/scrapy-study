# 链接提取器

链接提取器 `scrapy.CrawlSpider` 爬虫可以按照规则自动获取连接。

## 创建爬虫

添加 `-t crawl` 参数创建 CrawlSpider 爬虫模版。

```bash
scrapy genspider -t crawl ds2 dushu.com
```

使用上面的命令生成的文件 `ds2.py` 内容如下：

```python
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Ds2Spider(CrawlSpider):
    name = 'ds2'
    allowed_domains = ['dushu.com']
    start_urls = ['http://dushu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return item
```

**注意：在 `CrawlSpider` 爬虫中，没有 `parse` 函数**

重点在 `rules` 中：

- rules 是一个元组或者是列表，包含的是 Rule 对象

- Rule 表示规则，其中包含 `LinkExtractor`, `callback` 和 `follow` 等参数

- `LinkExtractor`： 连接提取器，可以通过正则或者是 `xpath` 来进行 `url` 地址的匹配

- `callback`：表示经过连接提取器提取出来的 URL 地址响应的回调函数，可以没有，没有表示响应不会进行回调函数的处理

- `follow`：连接提取器提取的 URL 地址对应的响应是否还会继续被 rules 中的规则进行提取，`True` 表示会，`False` 表示不追踪

## 爬取读书网

- 定义一个规则，来进行列表页翻页，`follow` 需要设置为 `True`

- 定义一个规则，实现从列表页进入详情页，并且指定回调函数

- 在详情页提取需要的数据

```python
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
        image_url = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@src').get()
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
```

## 注意事项

- 除了用命令 `scrapy genspider -t crawl <爬虫名> <allowed_domail>` 创建一个 `CrawlSpider` 的模板，也可以手动创建

- `CrawlSpider` 中不能再有以 `parse` 为名的数据提取方法，该方法被 `CrawlSpider` 用来实现基础url提取等功能

- `Rule` 对象中 `LinkExtractor` 为固定参数，其他 `callback`、`follow` 为可选参数

- 不指定 callback 且 follow 为 `True` 的情况下，满足规则的 URL 还会被继续提取和请求

- 如果一个被提取的 URL 满足多个规则，那么会从规则中选择一个满足匹配条件的 Rule 执行

## LinkExtractor常见参数

- `allow`： 满足括号中的 `re` 表达式的 URL 会被提取，如果为空，则全部匹配

- `deny`： 满足括号中的 `re` 表达式的 URL 不会被提取，优先级高于`allow`

- `allow_domains`： 会被提取的链接的 domains (URL 范围)，如：`['hr.tencent.com', 'baidu.com']`

- `deny_domains`： 不会被提取的链接的 domains (URL 范围)

- `restrict_xpaths`： 使用 xpath 规则进行匹配，和 allow 共同过滤 URL，即 xpath 满足的范围内的 URL
  地址会被提取，如：`restrict_xpaths='//div[@class="pagenav"]'`

## Rule常见参数

- `LinkExtractor`：链接提取器，可以通过正则或者是 xpath 来进行 URL 地址的匹配
- `callback`：表示经过连接提取器提取出来的 URL 地址响应的回调函数，可以没有，没有表示响应不会进行回调函数的处理
- `follow`：连接提取器提取的 URL 地址对应的响应是否还会继续被 rules 中的规则进行提取，默认 `True` 表示会，`False` 表示不会
- `process_links`：当链接提取器 `LinkExtractor` 获取到链接列表的时候调用该参数指定的方法，这个自定义方法可以用来过滤 URL，且这个方法执行后才会执行 callback 指定的方法

