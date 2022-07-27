# 概念和工作流程

## 概念

[Scrapy](https://github.com/scrapy/scrapy) 是一个Python编写的开源网络爬虫框架。

它是一个被设计用于爬取网络数据、提取结构性数据的框架。

它允许我们编写少量代码，并能够数据的快速抓取。

> Scrapy 使用了Twisted['twɪstɪd]异步网络框架，可以加快我们的下载速度。
>
> Scrapy文档地址：[docs.scrapy.org](https://docs.scrapy.org/en/latest/)

## 工作流程

![](./images/scrapy-work-process.png)

其流程可以描述如下：

1. 爬虫中起始的 URL 构造成 Request 对象 --> 爬虫中间件 --> 引擎 --> 调度器
2. 调度器把 Request --> 引擎 --> 下载中间件 --> 下载器
3. 下载器发送请求，获取 Response 响应 --> 下载中间件 --> 引擎 --> 爬虫中间件 --> 爬虫
4. 爬虫提取 URL 地址，组装成 Request 对象 --> 爬虫中间件 --> 引擎 --> 调度器，重复步骤2
5. 爬虫提取数据 --> 引擎 --> 管道 -> 保存数据

> - 引擎 `Scrapy Engine`
> - 爬虫 `Spider`
> - 管道 `Item Pipeline`
> - 调度器 `Schedule`
> - 爬虫中间件 `Spider Middlewares`
> - 下载中间件 `Downloader Middlewares`

**注意：**

- 图中中文是为了方便理解后加上去的
- 图中绿色线条的表示数据的传递
- 注意图中中间件的位置，决定了其作用
- 注意其中引擎的位置，所有的模块之前相互独立，只和引擎进行交互

## 三个内置对象

- `Request` 请求对象：由 `url` `method` `post_data` `headers`等构成
- `Response` 响应对象：由 `url` `body` `status` `headers`等构成
- `Item` 数据对象：对字典的封装

## 模块具体作用

| 名称                             | 作用                                  | 备注           |
|--------------------------------|-------------------------------------|--------------|
| `Scrapy Engine` 引擎             | 总指挥，负责数据和信号在不同模块之间的传递、协调            | Scrapy 框架已实现 |
| `Schedlue` 调度器                 | 一个队列，存放引擎提交的 Request 请求。先进先出 FIFO   | Scrapy 框架已实现 |
| `Downloader` 下载器               | 接收引擎提交的 Reqeust 请求，并将响应返回给引擎        | Scrapy 框架已实现 |
| `Spider` 爬虫                    | 处理引擎传递的 Response，提取数据，提交 URL，并提交给引擎 | **需要编写代码逻辑** |
| `Item Pipeline` 管道             | 处理引擎传过来的数据，比如存储                     | **需要编写代码逻辑** |
| `Downloader Middlewares` 下载中间件 | 可以自定义的下载扩展，比如设置代理IP                 | 一般无需编写代码逻辑   |
| `Spider Middlewares` 爬虫中间件     | 可用于自定义 Requests 请求和 Response 过滤     | 一般无需编写代码逻辑   |

> 爬虫中间件和下载中间件只是运行逻辑的位置不同，作用是重复的，比如替换`User-Agent` 等。