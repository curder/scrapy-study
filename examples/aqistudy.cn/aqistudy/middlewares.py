# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

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
