# 爬取一些网站的图片、小说、视频

------

本项目主要用于一些网站的妹子图片爬取，以及某小视频网站的视频、小说，利用工厂模式编写，方便日后扩展。

目前为初级版本，仅仅可以爬取 [di81美女网](http://di81.com/) 、[mzitu](http://www.mzitu.com/) 的图片；[001mao]()的图片、小说、视频（***001mao网站的链接不能给出，怕csdn屏蔽，欢迎去github，代码内有链接***）。

还有许多需要改进的地方，如免费代理模块未做可扩展处理、mongoDb安全性处理模块。该小项目会不定时更新，欢迎star
详细介绍，请看我的博客：https://blog.csdn.net/linhai1028/article/details/80280674

------

## 模块简介

httpProxy.py 模块爬取网络上的免费代理ip网站，并验证可用后入库，而后进行实时验证。

crawBase.py 工厂模式中的产品模块的基类模块，主要利用requests做请求，lxml做页面分析。

crawMzitu.py 爬取 [mzitu](http://www.mzitu.com/) 网站的妹子的图片，该网站有反爬虫，解决方式 请求头里添加**Reference**

crawdi81.py 爬取 [di81美女网](http://di81.com/) 的妹子图片

craw001maoPic.y  爬取 [001mao]() 的妹子图片 

craw001maoXs.py 爬取 [001mao]() 的小说

craw001maoDy.py 爬取 [001mao]() 的小视频

log.py 做日志输出处理。

xmFactory.py 工厂模式中的工厂模块。

xmCustomer.py 工厂模式中的客户模块。

mongodb主要负责数据库的链接，切换到表明，以及数据库的插入操作，其他操作暂时没有封装。

## 结果展示

### 1.数据库展示

di81网站图片数据库表结构展示
![di81](pic/di81_1.png)

mzitu网站图片数据库表结构展示
![mzitu](pic/mzitu.png)

001maoPic网站图片数据库表结构展示
![mzitu](pic/001maoPic.png)

001maoDy网站小视频数据库表结构展示
![mzitu](pic/001maoDy.png)

001maoXs网站小说数据库表结构展示
![mzitu](pic/001maoXs.png)


2.图片展示

![这里写图片描述](pic/di81_2.png)
![这里写图片描述](pic/di81_3.png)

## 使用

安装相关的依赖包，依赖包需求见文末的环境部分
在mongoDb.py处配置数据库用户名和密码后，就可以运行代码了
```
python xmCustomer.py
```

-----

## 环境
1. python3.6
2. requests2.18
3. mongodb2.6
4. pymongo3.6
5. lxml4.2




