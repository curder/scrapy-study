# Scrapy Basic Demo

项目创建流程：

```bash
pip3 install Scrapy # 安装 Scrapy
scrapy startproject basic # 创建项目

scrapy genspider get baidu.com  # 创建蜘蛛文件
```


启动爬虫

```bash
scrapy crawl get  # 获取响应中单个内容，获取响应中input元素的值

scrapy crawl getall  # 获取响应中多个内容，获取响应中书本名称列表

scrapy crawl post  # 发送POST请求获取JSON响应
```

## 项目安装

使用下面的命令进入到项目目录

```bash
cd basic
```

创建一个虚拟环境
```bash
python3 -m venv ./venv # 创建虚拟环境
```

激活虚拟环境

```bash
chmod +x ./venv/bin/activate
source ./venv/bin/activate 
```

升级依赖

```bash
pip3 install -r requirements.txt
```