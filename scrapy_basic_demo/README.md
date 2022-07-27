# Baidu Spider

项目创建流程：

```bash
pip3 install Scrapy # 安装 Scrapy
scrapy startproject scrapy_basic_demo # 创建项目

scrapy genspider get baidu.com  # 创建蜘蛛文件
```


启动爬虫

```bash
scrapy crawl get  # 获取响应中单个内容，获取响应中input元素的值

scrapy crawl getall  # 获取响应中多个内容，获取响应中书本名称列表
```