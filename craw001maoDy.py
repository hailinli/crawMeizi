# https://jzav-cloudflare.club/share/39Y8Yj0kv46wGAbw

# -*- coding: utf-8-*-
__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'

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
        self.xs001maoInfo = mongoDb.MongoDbOpreater('crawPorn', '001maoDy')
        self.num = 1
        # self.startUri = super(Craw001maoXs, self).startUri
        # self.baseUri = super()

    def saveXs(self, url):
        '''
        保存小说
        :return:
        '''
        r = requests.get(url, timeout=5).text  # 不要代理
        rd = {}
        rd['id'] = self.num
        sel = etree.HTML(r)
        xsDesc = sel.xpath('//span[@class="cat_pos_l"]/a')
        xsDesc = os.path.join(self.picDictory, xsDesc[1].text, xsDesc[2].text)
        rd['desc'] = xsDesc.split('/')[-1]
        rd['url'] = url
        rd['localPath'] = xsDesc
        insertTime =  time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        rd['insertTime'] = insertTime
        rd['content'] = r
        if self.pic001maoInfo.insert(rd):
            logg.info('success insert into mongo xs: %s' % url)
        else:
            logg.info('fail insert into mongo xs: %s' % url)


    def engin(self):
        # classUris = self.getFirstPage(self.startUri)
        # for classUri in classUris[8:16]:  # 得到分类,前8个为图片
        #     print(classUri)
        #     xsUris = self.getSecondPagePic(classUri)
        #     for xsUri in xsUris:
        #         self.saveXs(xsUri)
        self.logCrawPic('https://jzav-cloudflare.club/share/39Y8Yj0kv46wGAbw', {}, 't.mp4')

if __name__ == '__main__':
    craw001maoXs = Craw001maoDy()
    craw001maoXs.crawlRun()