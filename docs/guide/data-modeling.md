# 数据建模

通常在做项目的过程中，在 `items.py` 中进行数据建模，并以好对应要分析的页面字段。


## 为什么建模

- 定义 `Item` 即提前规划好哪些字段需要抓，防止手误，因为定义好之后，在运行过程中，系统会自动检查
- 配合代码注释可以清晰的知道要抓取哪些字段，没有定义的字段不能抓取，当目标字段较少时可使用字典 `dict` 代替
- 使用 `scrapy` 的一些特定组件需要 `Item` 做支持，如 `scrapy` 的 `ImagesPipeline` 管道类

## 如何建模

在项目的 `items.py` 文件中定义要提取的字段：

```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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

## 如何使用模板类

模板类定义以后需要在爬虫中导入并且实例化，之后的使用方法和使用字典相同


```python
import scrapy
from dushu.items import DushuItem

class DsSpider(scrapy.Spider):
    # ...

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
            author = author,
            publishing_house=publishing_house,
            description=description
        )
```