# Scrapy Redis 分布式爬虫

- [Github](https://github.com/rmax/scrapy-redis)

- [Usage](https://github.com/rmax/scrapy-redis/wiki/Usage)

项目创建流程：

```bash
pip3 install Scrapy scrapy-redis # 安装 Scrapy 和 Scrapy-redis
scrapy startproject scrapy_redis_example scrapy_redis_example # 创建项目

scrapy genspider -t crawl dmoz dmoz-odp.org  # 创建蜘蛛文件
scrapy genspider spider_redis spider_redis  # 创建Redis爬虫
scrapy genspider -t crawl crawler_redis crawler_redis # 创建链接提取器Redis爬虫
```

启动爬虫

```bash
scrapy crawl dmoz

scrapy crawl spider_redis # 启动监听爬虫
redis-cli -n 15 lpush spider:start_urls https://www.baidu.com # 向Redis中添加起始URL

scrapy crawl crawler_redis # 启动监听爬虫
redis-cli -n 15 lpush crawler:start_urls https://www.baidu.com # 向Redis中添加起始URL
```


## 项目安装

使用下面的命令进入到项目目录

```bash
cd scrapy_redis_example
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