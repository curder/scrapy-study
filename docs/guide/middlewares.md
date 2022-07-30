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

## 配合 Selenium

### 中间件中使用 Selenium

```python
import time
import re
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from scrapy.http.response.html import HtmlResponse


class AqiDownloadMiddleware(object):
    def process_request(self, request, spider):
        if "daydata.php" in request.url:  # 仅过滤日历史数据请求URL

            driver = self.get_selenium_driver()  # 创建浏览器
            # print(request.url)
            driver.get(request.url)

            time.sleep(1)  # 延迟 1 秒钟执行

            body = driver.page_source

            # with open('daydata.html', mode='w', encoding='utf-8') as f:
            #     f.write(body)

            body = self.prune_body(body).decode('utf-8')  # 删除干扰元素

            # with open('daydata_2.html', mode='w', encoding='utf-8') as f:
            #     f.write(body)

            driver.close()

            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def prune_body(self, body):
        dom = etree.HTML(body)
        # 删除不应该展示数据的table的dom节点
        for element in dom.xpath("//table[contains(@style, 'position: absolute;')]"):
            element.getparent().remove(element)

        class_name_lists = re.compile(r'\.([a-z0-9A-Z]+?) \{.*?display: none;.*?\}', re.S).findall(body)
        # 删除不应该展示的 th 和 td dom节点
        for class_name in class_name_lists:
            # print(class_name)
            for element in dom.xpath('//td[contains(@class, "%s")]' % class_name):
                element.getparent().remove(element)
            for element in dom.xpath('//th[contains(@class, "%s")]' % class_name):
                element.getparent().remove(element)
            for element in dom.xpath('//th[contains(@style, "display:none")]'):
                element.getparent().remove(element)
            for element in dom.xpath('//td[contains(@style, "display:none")]'):
                element.getparent().remove(element)
            for element in dom.xpath('//th[contains(@class, "hidden-lg")]'):
                element.getparent().remove(element)
            for element in dom.xpath('//td[contains(@class, "hidden-lg")]'):
                element.getparent().remove(element)
            for element in dom.xpath('//th[@class="hidden"]'):
                element.getparent().remove(element)
            for element in dom.xpath('//td[@class="hidden"]'):
                element.getparent().remove(element)

        return etree.tostring(dom)

    def get_selenium_driver(self):
        options = ChromeOptions()
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
        options.add_experimental_option("prefs",
                                        {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_argument('--incognito')  # 无痕隐身模式
        options.add_argument("disable-cache")  # 禁用缓存
        options.add_argument('disable-infobars')  # 禁用“chrome正受到自动测试软件的控制”提示
        options.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
        # options.add_argument("--headless")  # 无头模式--静默运行
        options.add_argument("--window-size=1920,1080")  # 使用无头模式，需设置初始窗口大小
        options.add_argument("--test-type")
        options.add_argument("--ignore-certificate-errors")  # 与上面一条合并使用；忽略 Chrome 浏览器证书错误报警提示
        options.add_argument("--disable-gpu")  # 禁用GPU加速
        options.add_argument('--no-sandbox')
        options.add_argument("--no-first-run")  # 不打开首页
        options.add_argument("--no-default-browser-check")  # 不检查默认浏览器
        options.add_argument('--start-maximized')  # 最大化
        options.add_argument('--disable-gpu')  # 禁用GPU加速
        options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        return Chrome(options=options)
```

### 爬虫代码 `aqi.py`

```python
import scrapy
from lxml import etree
from xml.etree.ElementTree import tostring
from ..items import AqiItem


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    def parse(self, response):
        city_node_list = response.xpath('//div[@class="all"]/div[@class="bottom"]/ul//li/a')  # 获取城市月份节点

        for city_node in city_node_list[16:17]:  # 获取一个城市
            url = response.urljoin(city_node.xpath('./@href').get())
            city_name = city_node.xpath('./text()').get()
            # print(url, city_name)
            yield scrapy.Request(url=url, callback=self.parse_month_data, meta={"city_name": city_name})

    # 获取空气质量指数月统计历史数据，分析出日统计历史数据页面地址
    def parse_month_data(self, response):
        month_node_list = response.xpath('//ul[@class="unstyled1"]/li/a/@href').getall()  # 获取城市日节点
        for month_url in month_node_list:  # 获取12个月
            url = response.urljoin(month_url)
            yield scrapy.Request(url=url, callback=self.parse_day_data, meta={"city_name": response.meta['city_name']})

    def parse_day_data(self, response):
        # 分析数据
        first_table_tr = response.xpath("//table/tbody/tr[position() = 1]"
                                        "/*[local-name()='td' or local-name()='th']/text()")  # 获取随机数据表头，确定其索引
        table_tr_list = response.xpath('//table/tbody/tr[position() > 1]')  # 获取所有数据

        need_fields = {
            'day': "日期",
            'aqi': "AQI",
            'quality_level': "质量等级",
            'pm_2_5': 'PM2.5',
            'pm_10': 'PM10',
            'co': 'CO',
            'so2': 'SO2',
            'no2': 'NO2',
            'o3_8h': 'O3_8h'
        }

        reverse_need_fields = {v: k for k, v in need_fields.items()}  # 反转字典，将key -> value 互换

        # print(first_table_tr.getall())

        need_field_dict = {reverse_need_fields[table_th.get()]: index + 1 for index, table_th in
                           enumerate(first_table_tr)
                           if table_th.get() in need_fields.values()}  #

        # print(need_field_dict)

        for table_tr in table_tr_list:
            # tr = table_tr.get()

            yield AqiItem(
                city_name=response.meta['city_name'],
                day=table_tr.xpath('./td[%d]/text()' % need_field_dict['day']).get(),
                aqi=table_tr.xpath('./td[%d]/text()' % need_field_dict['aqi']).get(),
                quality_level=table_tr.xpath('./td[%d]//text()' % need_field_dict['quality_level']).get(),
                pm_2_5=table_tr.xpath('./td[%d]/text()' % need_field_dict['pm_2_5']).get(),
                pm_10=table_tr.xpath('./td[%d]/text()' % need_field_dict['pm_10']).get(),
                co=table_tr.xpath('./td[%d]/text()' % need_field_dict['co']).get(),
                so2=table_tr.xpath('./td[%d]/text()' % need_field_dict['so2']).get(),
                no2=table_tr.xpath('./td[%d]/text()' % need_field_dict['no2']).get(),
                o3_8h=table_tr.xpath('./td[%d]/text()' % need_field_dict['o3_8h']).get(),
            )
```

### 数据建模 `items.py`

```python
import scrapy

class AqiItem(scrapy.Item):
    city_name = scrapy.Field()  # 城市名
    day = scrapy.Field()  # 日期
    aqi = scrapy.Field()  # AQI
    quality_level = scrapy.Field()  # 质量等级
    pm_2_5 = scrapy.Field()  # PM2.5
    pm_10 = scrapy.Field()  # PM10
    co = scrapy.Field()  # CO
    so2 = scrapy.Field()  # SO2
    no2 = scrapy.Field()  # NO2
    o3_8h = scrapy.Field()  # O3_8h
```

[完整项目参考这里](https://github.com/curder/scrapy-demo/blob/master/examples/aqistudy.cn/README.md)