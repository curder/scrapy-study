# 构造分页请求

当爬取一个页面同时需要分析其分页页面数据，比如：

![数据分页](./images/pagination.png)

## 实现分页思路

1. 找到分页的 `url` 地址；
2. 构造 URL 地址的请求对象，`scrapy.Request(url, callback)`
    - `url`：请求的URL地址
    - `callback`：指定解析函数名称，表示该请求返回的响应使用对应函数进行解析
3. 传递给引擎 `yield scrapy.Request(url,callback)`

## 构造 Request 对象

下面以爬取[读书网](https://www.dushu.com/book/1617.html)为例了解如何实现翻页请求。

### 简单配置项目

修改 `settings.py` 基础配置：

```python
# False表示忽略网站的robots.txt协议，默认为True
ROBOTSTXT_OBEY = False

# scrapy发送的每一个请求的默认UA都是设置的这个User-Agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
```

### 爬虫代码实现

在爬虫文件的 `parse` 方法中提取分页链接并构建 Request 对象：

```python
import scrapy


def parse(self, response):
    # ...
    # 提取分页链接
    page_list = response.xpath('////div[@class="pages"]//a/@href').getall()
    for href in page_list:
        url = 'https://www.dushu.com' + href
        yield scrapy.Request(url=url, callback=self.parse)
```

### Request 参数说明

Request 对象的更多参数：`scrapy.Request(url[,callback,method="GET",headers,body,cookies,meta,dont_filter=False])`

**参数说明：**

- 中括号里的参数为可选参数

- `callback`：表示当前的url的响应交给哪个函数去处理

- `meta`：实现数据在不同的解析函数中传递，meta 默认带有部分数据，比如下载延迟，请求深度等

- `dont_filter`：
  默认为False，会过滤请求的url地址，即请求过的url地址不会继续被请求，对需要重复请求的url地址可以把它设置为Ture，比如贴吧的翻页请求，页面的数据总是在变化;start_urls中的地址会被反复请求，否则程序不会启动

- `method`：指定POST或GET请求

- `headers`：接收一个字典，其中不包括cookies

- `cookies`：接收一个字典，专门放置cookies

- `body`：接收json字符串，为POST的数据，发送payload_post请求时使

#### meta 参数

`meta` 的作用：可以实现数据在不同的解析函数中的传递

在爬虫文件的 `parse` 方法中，提取详情页增加之前 `callback` 指定的 `parse_detail` 函数：

```python
import scrapy


def parse(self, response):
    # ...
    yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={"item": item})
# ...
```

```python
def parse_detail(self, response):
    # 获取之前传入的item
    item = resposne.meta["item"]
```

**特别注意**

- `meta` 参数是一个字典

- `meta` 字典中有一个固定的键 `proxy`，表示代理 `ip`

## 参考代码

蜘蛛文件`dushu.com/dushu/spiders/ds.py` 内容：

```python
import scrapy
from dushu.items import DushuItem


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
        id = response.url.strip('/').split('/')[-1]
        title = response.xpath('//div[@class="book-title"]/h1/text()').get()
        image_url = response.xpath('//div[@class="book-pic"]/div[@class="pic"]/img/@src').get()
        price = response.xpath('//p[@class="price"]/span[@class="num"]/text()').get('0')
        author = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[1]/td[2]/text()').get('')
        publishing_house = response.xpath('//div[@class="book-details-left"]/table/tbody/tr[2]/td[2]/text()').get()
        description = response.xpath("//div[@class='book-summary'][1]//div[@class='text txtsummary']/text()").get('')

        yield DushuItem(
            id=id,
            title=title,
            image_url=image_url,
            price=price,
            author=author,
            publishing_house=publishing_house,
            description=description
        )
```

模型文件 `dushu.com/items.py` 内容：

```python
import scrapy


class DushuItem(scrapy.Item):
    id = scrapy.Field()  # 课本ID
    title = scrapy.Field()  # 书本名
    image_url = scrapy.Field()  # 书本URL链接
    price = scrapy.Field()  # 书本价格
    author = scrapy.Field()  # 作者
    publishing_house = scrapy.Field()  # 出版社
    description = scrapy.Field()  # 内容简介
```

配置文件 `dushu.com/settings.py` 内容：

```python
# ...
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = False
# ...
```