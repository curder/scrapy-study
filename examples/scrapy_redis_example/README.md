# Scrapy Redis 分布式爬虫

项目创建流程：

```bash
pip3 install Scrapy scrapy-redis # 安装 Scrapy 和 Scrapy-redis
scrapy startproject scrapy_redis_example scrapy_redis_example # 创建项目

scrapy genspider -t crawl dmoz dmoz-odp.org  # 创建蜘蛛文件
scrapy genspider spider_redis spider_redis  # 创建Redis爬虫
```

启动爬虫

```bash
scrapy crawl dmoz

scrapy crawl spider_redis # 启动监听爬虫
redis-cli -n 15 lpush aspider_redis:start_urls https://www.baidu.com # 向Redis中添加起始URL
```