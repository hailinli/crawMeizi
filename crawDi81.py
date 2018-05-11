# -*- coding: utf-8-*-
__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'

import os
import random
import time

import requests
from lxml import etree

import log
import logging
log.initLogConf()
logg = logging.getLogger(__file__)
import crawBase
import mongoDb


class CrawDi81(crawBase.CrawMzBase):

    def __init__(self):
        super(CrawDi81, self).__init__()
        self.urlBase = 'http://www.di81.com/'
        self.startUrl = 'http://www.di81.com/PicList/'
        # mongodb = mongoDb.MongoDbOpreater('crawMeizi', 'di81')
        # self.di81Info = mongodb.getTableOpreater()
        self.di81Info = mongoDb.MongoDbOpreater('crawMeizi', 'di81')
        self.num = 1


    def getPicUri(self, url):
        '''
        解析二级页面,得到图片链接
        :return:
        '''
        r = requests.get(url, headers=self.headers , timeout=5).content
        sel = etree.HTML(r)
        pngUris = sel.xpath('//img/@src')
        # print(pngUris)
        return pngUris


    def _crawl(self, url, params={}):
        '''
        爬取妹子页面,并解析得到相关信息,包括二级页面的链接
        :param url:
        :param sq:
        :return:
        '''
        self.headers = {'User-Agent': random.choice(self.user)}  # 更新头
        r = requests.get(url, headers=self.headers, params=params, timeout=5).content  # 不要代理
        sel = etree.HTML(r)

        desc = sel.xpath('//li/a/img/@alt')
        uris = sel.xpath('//li/span/a/@href')
        time = sel.xpath("//li/span[@class='time']")
        time = list(map(lambda x:x.text, time))
        view = sel.xpath("//li/span[@class='view']")
        view = list(map(lambda x:x.text, view))
        self._dataInsertDb(desc, uris, time, view)


    def _dataInsertDb(self, desc, uris, urITime, view):
        '''
        获取二级页面的数据链接,并将一级页面的数据与二级页面的链接入库
        :param desc:
        :param uris:
        :param urITime:
        :param view:
        :return:
        '''
        for i,subUri in enumerate(uris):
            subUriFull = self.urlBase + subUri
            # 从二级页面获取图片链接列表
            l = self.getPicUri(subUriFull)
            l = list(map(lambda x : self.urlBase + x, l))
            for u in l:
                rd = {}
                rd['id'] = self.num
                rd['sourcePicUrl'] = u
                rd['uriTime'] = urITime[i]
                rd['view'] = view[i]
                rd['desc'] =desc[i]
                name = u.split('/')[-1]
                if name == 'footer.gif':
                    continue
                insertTime =  time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
                rd['insertTime'] = insertTime

                f = os.path.join(self.picDictory, rd['desc'], name)
                rd['localPath'] = f
                # print(f)
                # print(rd)
                self.di81Info.insert(rd)
                self.num += 1
                dic = '%s/%s' %(self.picDictory, rd['desc'])
                if not os.path.exists(dic):
                    os.system('mkdir ' + dic)
                self.logCrawPic(u, {}, f)


    def _secureCrawl(self, url, params, total=3):
        '''
        安全抓取di81妹子html页面
        :param url:
        :return:
        '''
        try:
            self._crawl(url, params)
        except Exception as e:
            logg.warn(e)
            if total>0:
                return self._secureCrawl(url, params, total-1)
            return False
        return True


    def logCrawl(self, url, params):
        '''
        爬取妹子页面打日志
        :param url:
        :param sq:
        :return:
        '''
        if self._secureCrawl(url, params):
            logg.info(u'MZ页面爬取成功: %s' %url)
            return True
        else:
            logg.info(u'MZ页面爬取失败: %s'% url)
            return False


    def crawlRun(self):
        for i in range(1,18):
            params = {
                'typeid': '6',
                'pageindex' : str(i)
            }
            self.logCrawl(self.startUrl, params)
        for i in range(1,15):
            params = {
                'typeid': '7',
                'pageindex' : str(i)
            }
            self.logCrawl(self.startUrl, params)


if __name__ == '__main__':
    crawDi81 = CrawDi81()
    crawDi81.crawlRun()