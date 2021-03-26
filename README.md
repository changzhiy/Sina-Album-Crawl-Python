# Sina-Album-Crawl-Python
## 产品简介

:star:一款基于Python的简单好用的新浪微博相册爬虫，所需参数全部可输入，便于使用。

## 完善进度
  - 问题一：进度条功能 :+1:已解决
  - 问题二：起始页，中止页的功能 :+1:已解决
  - 问题三：健壮性不强 :+1:已解决一个照片不存在的bug，别的还没遇到过
  - 问题四：爬虫效率低 :-1: 未解决，目前解决方案为采用多线程的方式(写代码时减少，需要时间)
  - 2021/3/26 问题四 :+1:已解决，采用协程和协程池
  - 问题五：协程池未执行完程序就结束 :+1:已解决 在for循环之后使用pool.join()方法

## 环境简介
- python 3.8
- requests 库 
- re 库
- urlencode 库
- BeautifulSoup 库
- uuid 库 为文件取名
- math 库 
- sys 库
- fake_useragent库 使用多agent访问，避免被对方服务器关闭连接
- gevent库 开启协程 
  
## 使用方法概述
1. 获取参数
  访问程序中提供的链接，F12进入network模块，寻找get_all?开头的信息，查询Parameters参数
  ![image](https://user-images.githubusercontent.com/63215608/111478595-2f50b180-876b-11eb-8b9b-cdc9657435dc.png)
  
2.运行程序，填写信息
![image](https://user-images.githubusercontent.com/63215608/111477885-843ff800-876a-11eb-9dc3-69506f6ba87e.png)
