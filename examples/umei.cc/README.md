# 使用 Scrapy 下载图片

## 项目准备

> ⚠️⚠️⚠️**注意：** 下载图片功能依赖 `Pillow` 组件，使用 `pip` 下载。

```bash
pip install Scrapy Pillow
```


```bash
srapy startproject umei umei.cc   # 创建项目
scrapy genspider download_images umei.cc  # 创建蜘蛛文件
```

## 数据建模

数据建模文件：`items.py`，中编写 `image_urls` 和 `images` 字段

```python {6-7}
import scrapy

class UmeiItem(scrapy.Item):
    id = scrapy.Field()  # 详情ID

    image_urls = scrapy.Field()  # 存储图片URL
    images = scrapy.Field()  #
```

## 爬虫修改

爬虫文件：`umei/spiders/download_images.py`

```python
import re

import scrapy
import hashlib
from ..items import UmeiItem
from scrapy.utils.python import to_bytes
from scrapy_redis.spiders import RedisSpider


class DownloadImagesSpider(RedisSpider):
    name = 'download_images'
    # allowed_domains = ['umei.cc', 'shanghai-jiuxin.com', 'zutuanla.com']
    # start_urls = ['https://www.umei.cc/meinvtupian/meinvxiezhen/']
    redis_key = 'download_images:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(DownloadImagesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 1. 分析目标页面图片列表，找到图片详情页
        image_detail_urls = response.xpath('//ul[contains(@class, "pic-list")]/li/a/@href').getall()
        for url in image_detail_urls[:1]:
            id = self.get_page_id(url)
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_image_detail, meta={"id": id})

    # 处理页面详情
    def parse_image_detail(self, response):
        # 1. 分析下一页图片详情和其他组图片地址
        xpath = '//div[@class="gongneng"]//a/@href|//div[@class="img-box"]/following-sibling::a/@href'
        next_page_urls = response.xpath(xpath).getall()
        for url in next_page_urls:
            id = self.get_page_id(url)
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_image_detail,
                meta={"id": id}
            )

        # 2. 分析出页面中待下载的图片地址
        image_url = response.xpath('//section[@class="img-content"]//img/@src').get()
        item = UmeiItem()
        item['id'] = response.request.meta['id']

        item['image_url'] = image_url.replace('http://kr.shanghai-jiuxin.com/', 'https://kr.zutuanla.com/')

        item['path'] = f'origin/{item["id"]}-{hashlib.sha1(to_bytes(image_url)).hexdigest()}.jpg'

        yield item

    def get_page_id(self, url):
        return re.compile(r'(?P<id>\d+)(_\d+)*.htm', re.S).search(url).group('id')
```

## 项目设置

配置文件：`settings.py`

```python
# 设置重复过滤模块
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 设置调度器，scrapy_redis中的调度器具备和数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 设置当爬虫结束时是否保存 Redis 数据库中是否去重集合与任务队列
SCHEDULER_PERSIST = True

# 添加中间件用于图片下载
ITEM_PIPELINES = {
    'umei.pipelines.UmeiPipeline': 300,

    # 当开启该管道，该管道会将数据存储到 Redis 数据库中
    'scrapy_redis.pipelines.RedisPipeline': 400,
    # 'scrapy.pipelines.images.ImagesPipeline': 300,
}
DEFAULT_IMAGES_URLS_FIELD = 'image_url'
IMAGES_STORE = 'images'
# IMAGES_THUMBS = {
#     'small': (100, 100),
#     'big': (340, 340),
# }
IMAGES_EXPIRES = 90  # 文件过期延迟 90 天

DOWNLOAD_DELAY = 0.5

# 项目管道序列化并存储此redis密钥中的项目。
REDIS_ITEMS_KEY = 'www.umei.cc:meinvtupian:meinvxiezhen:items'

# 指定连接到Redis时要使用的主机和端口（可选）。
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
```

## 添加自定义管道

默认的管道类 `scrapy.pipelines.images.ImagesPipeline` 存储的文件名不满足需求，通过自定义管道类 `pipelines.py` 中编写自定义逻辑：

```python
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class UmeiPipeline(ImagesPipeline):
    """自定义图片下载器, 添加资源ID作为文件夹保存图片"""

    def get_media_requests(self, item, info):
        """发生图片下载请求"""
        yield scrapy.Request(item["image_url"], meta={"path": item['path']})  # 继续传递图片存储路径

    def file_path(self, request, response=None, info=None, *, item=None):
        """自定义图片保存路径"""
        return request.meta['path']
```

# 启动爬虫

```bash
scrapy crawl download_images
redis-cli -n 1 LPUSH download_images:start_urls '{"url": "https://www.umei.cc/meinvtupian/meinvxiezhen/"}' # 向Redis中添加指定key
```

## 官方文档地址

- [Downloading and processing files and images¶](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)