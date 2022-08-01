# [dangdang.com](https://category.dangdang.com)

项目创建流程：

```bash
pip3 install Scrapy # 安装 Scrapy
scrapy startproject dangdang dangdang.com # 创建项目

scrapy genspider book dangdang.com  # 创建蜘蛛文件
scrapy genspider book_redis dangdang.com  # 创建分布式爬虫蜘蛛文件
```

启动爬虫

```bash
scrapy crawl book

scrapy crawl book_redis
redis-cli -n 15 LPUSH book_redis:start_urls '{"url": "https://category.dangdang.com/"}'
```

## 项目安装

使用下面的命令进入到项目目录

```bash
cd redis_examples
```

创建一个虚拟环境

```bash
python3 -m venv ./venv # 创建虚拟环境
```

激活虚拟环境

```bash
chmod +x ./venv/bin/activate
source ./venv/bin/activate 
```

升级依赖

```bash
pip3 install -r requirements.txt
```

## Scrapy Redis 分布式爬虫改造

1. 在蜘蛛文件导入 `RedisSpider` 爬虫类
2. 自定义蜘蛛文件继承自 `RedisSpider` 爬虫类
3. 注销爬虫类中 `allowed_domains` 和 `start_urls` 属性配置
4. 爬虫类中设置 `redis_key` 值
5. 设置爬虫类中 `__ini__` 方法
   ```python
   # 1. 导入 RedisSpider 爬虫类
    from scrapy_redis.spiders import RedisSpider

    class BookSpider(RedisSpider): # 2. 继承自RedisSpider 爬虫类
        name = 'book'  
        # 3. 注销爬虫类中 `allowed_domains` 和 `start_urls` 属性配置
        # allowed_domains = ['dangdang.com']
        # start_urls = ['https://category.dangdang.com/']

        # 4. 爬虫类中设置 `redis_key` 值 
        redis_key = 'book:start_urls'

        # 5. 设置爬虫类中 `__ini__` 方法
        def __init__(self, *args, **kwargs):
            # Dynamically define the allowed domains list.
            domain = kwargs.pop('domain', '')
            self.allowed_domains = list(filter(None, domain.split(',')))
            super(BookSpider, self).__init__(*args, **kwargs)
   
        # ...
   ```
6. 配置项目自定义配置
   ```python
   import logging
   
   # 项目自定义配置

   USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

   # 设置重复过滤模块
   DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
   # 设置调度器，scrapy_redis中的调度器具备和数据库交互的功能
   SCHEDULER = "scrapy_redis.scheduler.Scheduler"
   # 设置当爬虫结束时是否保存 Redis 数据库中是否去重集合与任务队列
   SCHEDULER_PERSIST = True
   ITEM_PIPELINES = {
       # 'dangdang.pipelines.ScrapyRedisExamplePipeline': 300,
       # 当开启该管道，该管道会将数据存储到 Redis 数据库中
       'scrapy_redis.pipelines.RedisPipeline': 400,
   }
   # 日志级别
   LOG_LEVEL = logging.DEBUG

   # 引入人工延迟以利用并行性。加快爬行速度
   DOWNLOAD_DELAY = 1

   # 项目管道序列化并存储此redis密钥中的项目。
   REDIS_ITEMS_KEY = '%(spider)s:items'

   # 默认情况下，items序列化器是ScrapyJSONEncoder。您可以使用指向可调用对象的任何可导入路径。
   REDIS_ITEMS_SERIALIZER = 'json.dumps'

   # 指定连接到Redis时要使用的主机和端口（可选）。
   REDIS_HOST = 'localhost'
   REDIS_PORT = 6379
   REDIS_DB = 15

   # 更多Redis相关设置查看这里：https://github.com/rmax/scrapy-redis/wiki/Usage
   ```