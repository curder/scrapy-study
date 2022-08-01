# Scrapy settings for dangdang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging

BOT_NAME = 'dangdang'

SPIDER_MODULES = ['dangdang.spiders']
NEWSPIDER_MODULE = 'dangdang.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'dangdang (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'dangdang.middlewares.DangdangSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'dangdang.middlewares.DangdangDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'dangdang.pipelines.DangdangPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

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
# REDIS_ITEMS_SERIALIZER = 'json.dumps'

# 指定连接到Redis时要使用的主机和端口（可选）。
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 15

# 更多Redis相关设置查看这里：https://github.com/rmax/scrapy-redis/wiki/Usage
