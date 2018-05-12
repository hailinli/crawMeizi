# -*- coding: utf-8-*-
__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月12日'

import os
import time
import requests
from lxml import etree

import log
import logging
log.initLogConf()
logg = logging.getLogger(__file__)
import mongoDb
import craw001maoPic

class Craw001maoDy(craw001maoPic.Craw001maoPic):
    '''
    爬取001mao网站里的小说
    '''
    def __init__(self):
        super(Craw001maoDy, self).__init__()
        self.dy001maoInfo = mongoDb.MongoDbOpreater('crawPorn', '001maoDy')
        self.num = 1
        # self.startUri = super(Craw001maoXs, self).startUri
        # self.baseUri = super()

    def insertVideoDb(self, videoUris, videoPics, videoDescs, classon):
        '''
        保存视频信息
        :return:
        '''
        for i, c in enumerate(videoUris):

            rd = {}
            rd['id'] = self.num
            rd['class'] = classon
            rd['desc'] = videoDescs[i]
            rd['videoUrl'] = c
            rd['videoFengmian'] = videoPics[i]
            insertTime =  time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
            rd['insertTime'] = insertTime
            # print(rd)
            self.num += 1
            if self.dy001maoInfo.insert(rd):
                logg.info('success insert into mongo xs: %s' % c)
            else:
                logg.info('fail insert into mongo xs: %s' % c)

    def getVideoInfo(self, url):
        '''
        保存电影信息
        :param url:
        :return:
        '''
        r = requests.get(url, timeout=5).text  # 不要代理

        sel = etree.HTML(r)
        videoUris = sel.xpath('//div[@class="box dy_list"]/ul/li/a/@href')
        videoUris = list(map(lambda x:self.baseUri+x , videoUris))
        # print(xsDescs)
        videoPics = sel.xpath('//div[@class="box dy_list"]/ul/li/a/img/@src')
        videoDescs = sel.xpath('//div[@class="box dy_list"]/ul/li/a/h3')
        videoDescs = list(map(lambda x:x.text , videoDescs))
        classon = sel.xpath('//span[@class="cat_pos_l"]/a')[1].text
        # print(videoUris)
        # print(videoPics)
        # print(videoDescs)
        self.insertVideoDb(videoUris, videoPics, videoDescs, classon)

    def engin(self):
        classUris = self.getFirstPage(self.startUri)
        for classUri in classUris[16:24]:  # 得到分类,前8个为图片
            cls = self.classUriGen(classUri)
            for cl in cls:
                self.getVideoInfo(cl)
                print(cl)
        #     xsUris = self.getSecondPagePic(classUri)
        #     for xsUri in xsUris:
        #         self.saveXs(xsUri)

if __name__ == '__main__':
    craw001maoXs = Craw001maoDy()
    craw001maoXs.crawlRun()