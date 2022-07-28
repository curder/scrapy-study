# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import random
from dushu.settings import USER_AGENTS_LIST  # 从配置中导入UA列表


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS_LIST)


class CheckUA:
    def process_response(self, request, response, spider):
        print(request.headers['User-Agent'])
        return response  # 不能少！
