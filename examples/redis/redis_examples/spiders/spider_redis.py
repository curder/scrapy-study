from scrapy_redis.spiders import RedisSpider


class SpiderRedisSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'spider_redis'
    redis_key = 'spider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')

        self.allowed_domains = list(filter(None, domain.split(',')))
        super(SpiderRedisSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
