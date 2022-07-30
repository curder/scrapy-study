from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class CrawlerRedisSpider(RedisCrawlSpider):
    """Spider that reads urls from redis queue (crawler_redis:start_urls)."""
    name = 'crawler_redis'
    redis_key = 'crawler:start_urls'

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        print(self.allowed_domains)
        super(CrawlerRedisSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        yield {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
