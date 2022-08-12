# 使用 Scrapy 下载图片

## 项目准备

> **注意：** 下载图片功能依赖 `Pillow` 组件，使用 `pip` 下载。

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
from ..items import UmeiItem

def parse_image_detail(self, response):
    # ...
    
    # 2. 分析出页面中待下载的图片地址
    image_url = response.xpath('//section[@class="img-content"]//img/@src').get()
    item = UmeiItem()
    item['id'] = response.request.meta['id']

    item['image_urls'] = [image_url.replace('http://kr.shanghai-jiuxin.com/', 'https://kr.zutuanla.com/')]

    yield item
```

## 项目设置

配置文件：`settings.py`

```python
# ...

# 添加中间件用于图片下载
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 300}
IMAGES_STORE = 'images'  # 下载图片保存路径
# IMAGES_THUMBS = {
#     'small': (100, 100),
#     'big': (340, 340),
# }
IMAGES_EXPIRES = 90  # 文件过期延迟 90 天

DOWNLOAD_DELAY = 0.5
```

# 启动爬虫

```bash
scrapy crawl download_images
```

## 官方文档地址

- [Downloading and processing files and images¶](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)