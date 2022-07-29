# 中间件

根据 scrapy 运行流程中所在位置不同分为：

- 下载中间件

- 爬虫中间件

## 中间件的作用

预处理 Request 和 Response 对象

- 对 header 以及 cookie 进行更换和处理
- 使用代理 IP 等
- 对请求进行定制化操作

但在 scrapy 默认的情况下 两种中间件都在 `middlewares.py` 一个文件中，爬虫中间件使用方法和下载中间件相同，且功能重复，通常使用下载中间件。

## 方法

下载中间件的默认方法：

`process_request(self, request, spider)`。当每个 request 通过下载中间件时，该方法被调用。

- 返回 None 值：没有 return 也是返回 None ，该 request 对象传递给下载器，或通过引擎传递给其他权重低的 process_request 方法

- 返回 Response 对象：不再请求，把 response 返回给引擎

- 返回 Request 对象：把request对象通过引擎交给调度器，此时将不通过其他权重低的 process_request 方法

`process_response(self, request, response, spider)`。当下载器完成 http 请求，传递响应给引擎的时候调用

- 返回 Response：通过引擎交给爬虫处理或交给权重更低的其他下载中间件的 process_response 方法

- 返回 Request 对象：通过引擎交给调取器继续请求，此时将不通过其他权重低的 process_request 方法

- 在 `settings.py` 中配置开启中间件，权重值越小越优先执行

## 随机User-Agent

通过下载中间件随机 `User-Agent` 请求头。

1. 编写下载中间件逻辑
2. 在 `settings.py` 配置中添加UA列表
3. 在 `settings.py` 中启用中间件

### 编写中间件

编写中间件的逻辑在 `middlewares.py` 文件中：

```python
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
    def process_request(self, request, spider):  # 这里也可以通过 spider.name 判断爬虫名称对特定爬虫执行添加UA的操作
        request.headers['User-Agent'] = random.choice(USER_AGENTS_LIST)


class CheckUA:
    def process_response(self, request, response, spider):
        print(request.headers['User-Agent'])
        return response  # 不能少！
```

### 添加UA配置

在配置文件 `settings.py` 文件中配置对应的UA列表，方便统一修改和使用。

```python
# ...
USER_AGENTS_LIST = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
]
# ...
```

>
更多UA列表可以参考这里：[fengzhizi715/user-agent-list - GitHub](https://github.com/fengzhizi715/user-agent-list/blob/master/Chrome.txt)

### 启用中间件

在配置文件 `settings.py` 文件中配置下载中间件

```python
# ...
DOWNLOADER_MIDDLEWARES = {
    'dushu.middlewares.UserAgentMiddleware': 543,  # 543 是权重值
    'dushu.middlewares.CheckUA': 600,  # 先执行 543 权重的中间件，再执行 600 的中间件
}
# ...
```

## 随机代理IP

- 代理添加的位置下载中间件中的 `process_request` 方法中使用 `request.meta` 中增加 `proxy` 字段
- 获取一个代理 IP，赋值给 `request.meta['proxy']`
  1. 代理池中随机选择代理 IP 
  2. 代理ip的webapi发送请求获取一个代理 IP

代码实现：

- 中间件定义 `middlewares.py`
  ```python
  import random
  from dushu.settings import PROXY_LIST  # 从配置中导入UA列表
  
  class RandomProxyMiddleware(object):
      def process_request(self, request, spider):
          proxy = random.choice(PROXY_LIST)  # 可以在配置文件中读取，也可以从Redis中获取，或者通过API获取
  
          request.meta['proxy'] = proxy
          return None  # 可以不写 return
      def process_response(self, request, response, spider):
          if response.status != '200':
              request.dont_filter = True # 重新发送的请求对象能够再次进入队列
              return request
  ```

- 应用中间件和代理IP池 `settings.py`
  ```python
  DOWNLOADER_MIDDLEWARES = {
      'dushu.middlewares.RandomProxyMiddleware': 200,
      # ...
  }

  # 代理IP池
  PROXY_LIST = [
      'http://IP_ADDRESS:PORT',
      'http://ANOTHER_IP_ADDRESS:ANOTHER_PORT',
      # ...
  ]
  ```

扩展阅读：[Scrapy 爬免費代理(Proxy)](https://ithelp.ithome.com.tw/articles/10208575) 和 [[Day 24] Scrapy 隨機代理實現](https://ithelp.ithome.com.tw/articles/10208773)
