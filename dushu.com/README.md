# dushu.com

 获取[读书网](https://www.dushu.com/book/1617.html)中"国学入门"书籍列表的详情信息。
 
## 构建蜘蛛

```bash
scrapy genspider ds dushu.com  # 构建普通爬虫
scrapy genspider -t crawl ds2 dushu.com # 构建带链接提取器的爬虫
```


运行

```bash
scrapy crawl ds  # 使用普通爬虫

scrapy crawl ds2  # 使用链接提取器爬虫
```