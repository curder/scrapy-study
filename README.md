# Scrapy 学习

[![GitHub Pages](https://github.com/curder/scrapy-study/actions/workflows/build-docs.yml/badge.svg?branch=master)](https://curder.github.io/scrapy-study)

## [基础学习](examples/basic/README.md)

项目搭建、创建蜘蛛文件、pipeline管道使用、items使用等。

## [读书网站书本数据爬取](examples/dushu.com/README.md)

获取[读书网](https://www.dushu.com/book/1617.html) 中"国学入门"分类下的所有分页图片列表的书本详情信息。

## [PM2.5空气质量日历史数据获取爬虫](examples/aqistudy.cn/README.md)

[该站点](https://www.aqistudy.cn/historydata/)目前数据的目标页有一些反扒措施，比如数据使用JS动态加载，JS代码加密，禁用右键，禁用调试器查看源代码，Selenium 不能使用无头浏览器参数。

通过 `selenium` 在 Scrapy 的下载中间件发送请求并返回响应的响应清晰响应中的干扰数据，再将修改后的响应交给引擎。


## [scrapy-redis 分布式爬虫](examples/redis/README.md)

简单学习并初探 scrapy-redis 爬虫，感受从普通爬虫改造成 scrapy-redis 分布式爬虫的步骤和方法。


## 相关网站

- [Scrapy Docs](https://docs.scrapy.org/en/latest/)
- [Scrapy.org](https://scrapy.org/)