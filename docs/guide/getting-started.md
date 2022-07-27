# 入门使用

## 安装

**注意：** Scrapy 框架依赖 Python 版本需要 3.6+。

```bash
pip/pip3 install scrapy
```

> 建议进入到项目目录使用 `python3 -m venv .` 创建虚拟环境。

## 开发流程

1. 创建项目

   `scrapy startproject mySpider`

2. 创建爬虫

   `scrapy genspider ds dushu.com`

3. 提取数据

   根据网站结构在spider中实现数据采集相关内容

4. 保存数据

   使用pipeline进行数据后续处理和保存

## 创建项目

> 通过命令将 scrapy 项目的的文件生成出来，后续步骤都是在项目文件中进行相关操作，下面以抓取[读书网](https://www.dushu.com)的国学入门图书分类书籍列表为例来学习 scrapy
> 的入门使用：https://www.dushu.com/book/1617.html

创建scrapy项目的命令：

```bash
scrapy startproject <项目名字>
```

示例：

```bash
scrapy startproject dushu dushu.com
```

生成的目录和文件结果如下：

```text
➜  tree
.
└── dushu.com
    ├── dushu
    │   ├── __init__.py
    │   ├── items.py       ────> 自定义需要爬取的内容
    │   ├── middlewares.py ────> 自定义中间件文件
    │   ├── pipelines.py   ────> 管道，用于保存数据
    │   ├── settings.py    ────> 项目配置，请求头，管道启用等配置
    │   └── spiders
    │       └── __init__.py
    └── scrapy.cfg         ────> 项目配置文件
```

## 创建爬虫

通过命令创建出爬虫文件，爬虫文件为主要的代码逻辑文件，通常一个网站的爬取动作都会在爬虫文件中进行编写。

命令：
项目路径下执行:

```bash
scrapy genspider <爬虫名字> <允许爬取的域名>
```

> 爬虫名字: 作为爬虫运行时的参数
>
> 允许爬取的域名: 为对于爬虫设置的爬取范围，设置之后用于过滤要爬取的 URL ，如果爬取的 URL 与允许的域不同则被过滤掉。

示例：

```bash
cd dushu.com
scrapy genspider ds dushu.com
```

运行完创建爬虫文件命令后，会生成 `./dushu/spiders/ds.py` 文件。

## 编写逻辑

> 在上一步生成出来的爬虫文件 `ds.py` 中编写指定网站的数据采集操作，实现数据提取。

### 完善逻辑

在 `./dushu/spiders/ds.py` 中修改内容如下:

```python
import scrapy


class DsSpider(scrapy.Spider):
    name = 'ds'  # 爬虫名称
    allowed_domains = ['dushu.com']  # 允许爬取的范围
    start_urls = ['https://www.dushu.com/book/1617.html']  # 开始爬取的 URL 地址

    # 数据提取的方法，接受下载中间件传递的 Response
    def parse(self, response):
        # 提取书本详情链接，scrapy 的 Response 对象可以直接进行 xpath 操作
        href_list = response.xpath('//div[@class="book-info"]/div/a/@href').getall()
        for href in href_list:
            detail_url = 'https://www.dushu.com' + href
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    # 解析详情页逻辑
    def parse_detail(self, response):
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

**注意：**

- `scrapy.Spider` 爬虫类中必须存在 `parse` 方法
- 如果网站结构层次比较复杂，可以自定义其他解析函数
- 在解析函数中提取的 URL 地址如果要发送请求，则必须属于 `allowed_domains` 范围内，但是 `start_urls` 中的 `URL` 地址不受这个限制
- 启动爬虫的时候注意启动的位置，是在项目路径下启动
- `parse()` 方法中使用 `yield` 返回数据，且函数中的 yield 能够传递的对象只能是: `Request`, `items`, `dict`, `None`

### 定位元素以及提取数据、属性值的方法

解析并获取 scrapy 爬虫中的数据: 利用 xpath 规则字符串进行定位和提取

1. `response.xpath` 方法的返回结果是一个类似 `list` 的类型，其中包含的是 `Selector` 对象，操作和列表一样。但是有一些额外的方法
2. 额外方法 `getall()`：返回一个包含有字符串的列表
3. 额外方法 `get()`：返回列表中的第一个字符串，列表为空没有返回None

### Response 响应对象的常用属性

- `response.url`：当前响应的url地址
- `response.request.url`：当前响应对应的请求的url地址
- `response.headers`：响应头
- `response.requests.headers`：当前响应的请求头
- `response.body`：响应体，也就是html代码，byte类型
- `response.status`：响应状态码

## 保存数据

利用管道 pipelines 来处理(保存)数据。

### 开启管道支持

需要使用管道需要在项目的 `settings.py` 文件中开启管道配置。

```python
# settings.py文件中启用管道配置
ITEM_PIPELINES = {
    'dushu.pipelines.DushuPipeline': 300,
}
```

配置项中键为使用的管道类，管道类使用 `.` 进行分割。

第一个为项目目录，第二个为文件，第三个为定义的管道类。

配置项中值为管道的使用顺序，设置的数值约小越优先执行，该值一般设置为 `0` - `1000` 之间。

### 定义对数据的操作

定义一个管道类
重写管道类的process_item方法
process_item方法处理完item之后必须返回给引擎

```python
class DushuPipeline:
    # 爬虫文件中提取数据的方法每yield一次item，就会运行一次
    # 该方法为固定名称函数
    def process_item(self, item, spider):
        print(item)  # 仅打印引擎传递的值
        return item
```

- [数据存储到 json 文件 - docs.scrapy.org](https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-a-json-file)
- [数据存储到 MongoDB - docs.scrapy.org](https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb)

## 运行scrapy

命令：在项目目录下执行 `scrapy crawl <爬虫名称>`

```bash
scrapy crawl ds
```