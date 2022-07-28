# 管道 Pipelines

## 常用类方法

| 方法名                                |     | 说明                                                             |
|------------------------------------|:----|----------------------------------------------------------------|
| `process_item(self, item, spider)` |     | 1. 管道类中必须包含的函数<br />2. 实现对item数据的处理<br />3. 必须返回 `item`供其他管道使用 |
| `open_spider(self, spider)`        |     | 仅在爬虫开启的时执行一次                                                   |
| `close_spider(self, spider)`       |     | 仅在爬虫关闭的时执行一次                                                   |


## 管道文件的修改

管道文件在 `pipelines.py`

```python
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class DsPipeline:
    # 周期函数，当蜘蛛开始工作时触发
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'ds':
            self.file = open('ds.json', 'a', encoding='utf-8')

    # 周期函数，当蜘蛛结束工作时触发
    def colse_spider(self, spider):
        if spider.name == 'ds':
            self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'ds':
            print('PIPLINE: ', item)
            line = json.dumps(item, ensure_ascii=False) + "\n"
            self.file.write(line)
        return item  # 返回给下一个管道使用


class Ds2Pipeline:
    # 周期函数，当蜘蛛开始工作时触发
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'ds2':
            self.file = open('ds2.json', 'a', encoding='utf-8')

    # 周期函数，当蜘蛛结束工作时触发
    def colse_spider(self, spider):
        if spider.name == 'ds2':
            self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'ds2':
            print('PIPLINE: ', item)
            line = json.dumps(item, ensure_ascii=False) + "\n"
            self.file.write(line)
        return item  # 返回给下一个管道使用
```

1. 不同的 pipeline 可以处理不同爬虫的数据，通过 spider.name 属性来区分不同的爬虫

2. 不同的 pipeline 能够对一个或多个爬虫进行不同的数据处理的操作，比如一个进行数据清洗，一个进行数据的保存

3. 同一个管道类也可以处理不同爬虫的数据，通过 spider.name 属性来区分


## 开启管道

在 `settings.py` 设置开启 `ITEM_PIPELINES`

```python
# ...
ITEM_PIPELINES = {
    'dushu.pipelines.DsPipeline': 300, # 300 表示权重
    'dushu.pipelines.Ds2Pipeline': 301, # 权重值越小，越优先执行
}
# ...
```

## 使用注意事项

- 使用时需要在 `settings.py` 中开启

- pipeline 在 setting 中键表示位置（即pipeline在项目中的位置可以自定义），值表示距离引擎的远近，越近数据会越先经过：权重值小的优先执行

- 有多个 pipeline 的时候，`process_item` 方法必须 `return item`，否则后一个管道取到的数据为 None

- pipeline 中 `process_item` 的方法必须有，否则 `item` 没有办法接受和处理

- `process_item` 方法接受 item 和 spider，其中 spider 表示当前传递 item 过来的 spider

- `open_spider(spider)`：能够在爬虫开启的时候执行一次

- `close_spider(spider)`： 能够在爬虫关闭的时候执行一次

- 上述两个方法经常用于爬虫和数据库的交互，在爬虫开启的时候建立和数据库的连接，在爬虫关闭的时候断开和数据库的连接
