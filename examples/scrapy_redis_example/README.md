# Scrapy Redis 分布式爬虫

项目创建流程：

```bash
pip3 install Scrapy scrapy-redis # 安装 Scrapy 和 Scrapy-redis
scrapy startproject scrapy_redis_example scrapy_redis_example # 创建项目

scrapy genspider -t crawl dmoz dmoz-odp.org  # 创建蜘蛛文件
```
启动爬虫

```bash
scrapy crawl dmoz
```