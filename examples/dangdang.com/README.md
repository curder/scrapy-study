# [dangdang.com](https://category.dangdang.com)


项目创建流程：

```bash
pip3 install Scrapy # 安装 Scrapy
scrapy startproject dangdang dangdang.com # 创建项目

scrapy genspider book dangdang.com  # 创建蜘蛛文件
```

启动爬虫

```bash
scrapy crawl book
```


## 项目安装

使用下面的命令进入到项目目录

```bash
cd redis_examples
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

