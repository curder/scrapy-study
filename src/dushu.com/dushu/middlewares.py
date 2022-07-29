# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import random
from dushu.settings import USER_AGENTS_LIST, PROXY_LIST  # 从配置中导入UA列表


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS_LIST)


class CheckUA(object):
    def process_response(self, request, response, spider):
        print(request.headers['User-Agent'])
        return response  # 不能少！


class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXY_LIST)  # 可以在配置文件中读取，也可以从Redis中获取，或者通过API获取

        request.meta['proxy'] = proxy
        return None  # 可以不写 return

    def process_response(self, request, response, spider):
        if response.status != '200':
            request.dont_filter = True  # 重新发送的请求对象能够再次进入队列
            return request
