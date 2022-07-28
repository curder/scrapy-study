# 模拟登录

Scrapy 模拟登录的方式有：

1. 直接携带 `cookies`
2. 找 `URL` 地址，发送 `POST` 请求存储 `cookie`

下面以登录GitHub网站为例作展示。

## 直接携带 Cookies

1. 在地址栏登录github网站，在浏览器中获取到 `cookies` 值。
   ![Github Cookies](./images/github-cookies.png)

2. 通过重写爬虫的 `start_requests` 方法，将请求头中添加 `cookies`。

```python
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/settings/profile']

    def start_requests(self):
        # 在 Chrome 浏览器的调试工具中 Application -> Cookies -> https://github.com -> user_session
        cookies_str = 'user_session=oBOLKMa6wZD1Ai-xxx'
        cookies = {i.split('=')[0]: i.split('=')[-1] for i in cookies_str.split('; ')}
        # cookies = {}
        yield scrapy.Request(url=self.start_urls[0], cookies=cookies)

    def parse(self, response):
        print(response.url)
        # 登录成功打印：https://github.com/settings/profile
        # 没有登录打印：https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fsettings%2Fprofile
```

> **注意：** `scrapy` 中 `cookie` 不能够放在 `headers` 中，在构造请求的时候有专门的 `cookies` 参数，能够接受字典形式的 `cookies`