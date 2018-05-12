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

class Craw001maoPic(crawBase.CrawMzBase):
    def __init__(self):
        super(Craw001maoPic, self).__init__('001maoPic')
        self.startUri = 'http://www.001mao.com/'
        self.baseUri = 'http://www.001mao.com/'
        self.pic001maoInfo = mongoDb.MongoDbOpreater('crawPorn', '001maoPic')
        self.num = 1

    def getFirstPage(self, url):
        '''
        爬取网站第一页, 获得图片或者电影分类子页,以及对应的类型
        :return:
        '''
        self.headers = {
            'User-Agent': random.choice(self.user),
            'Referer': self.baseUri
        }  # 更新头
        r = self.get(url, headers=self.headers).content  # 不要代理
        if r == False:
            return []
        # print(r)
        sel = etree.HTML(r)
        classUris = sel.xpath("//li[@class='head-2a-list']/a/@href")
        classUris = list(map(lambda x:self.baseUri+x.strip(), classUris))
        classDescs = sel.xpath("//li[@class='head-2a-list']/a")
        classDescs = list(map(lambda x:x.text, classDescs))
        # print(classUris)
        # print(classDescs)
        return classUris

    def getSecondPagePic(self, url):
        '''
        得到所有二级页面的小分类图片链接
        :param url:
        :return:
        '''
        self.headers = {
            'User-Agent': random.choice(self.user),
            'Referer': self.baseUri
        }  # 更新头
        r = self.get(url, headers=self.headers, total=10).content  # 不要代理
        if r == False:
            return False
        # print(url)
        # print(r)
        sel = etree.HTML(r)
        picUris = sel.xpath('//div[@class="box list channel"]/ul/li/a/@href')
        picUris = list(map(lambda x:self.baseUri+x, picUris))
        # print(picUris)
        return picUris

    def getThirdPagePic(self, url):
        '''
        获得最终的图片链接,可直接下载
        :param url:
        :return:
        '''
        # self.headers = {
        #     'User-Agent': random.choice(self.user),
        #     'Referer': self.baseUri
        # }  # 更新头
        r = self.get(url, headers=self.headers, total=10).content  # 不要代理
        if r == False:
            return [], []
        sel = etree.HTML(r)
        # print(r)
        picUris = sel.xpath('//div[@class="content"]/p/img/@src')
        picThirdDesc = sel.xpath('//span[@class="cat_pos_l"]/a')
        picThirdDesc = os.path.join(self.picDictory, picThirdDesc[1].text.strip(), picThirdDesc[2].text.replace(' ', '').strip())
        # print(picUris)
        return picUris, picThirdDesc


    def engin(self):
        classUris = self.getFirstPage(self.startUri)
        for classUri in classUris[:8]:  # 得到分类,前8个为图片
            print(classUri)
            classUriSubs = self.classUriGen(classUri)
            for classUriSub in classUriSubs:
                picUris = self.getSecondPagePic(classUriSub)
                for picUri in picUris:
                    print(picUri)
                    thirdPicUris, thirdPicDesc = self.getThirdPagePic(picUri)
                    rd = {}
                    rd['id'] = self.num
                    rd['class'] = thirdPicDesc.split('/')[1]
                    rd['desc'] = thirdPicDesc.split('/')[-1]
                    rd['localPath'] = thirdPicDesc
                    insertTime =  time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
                    rd['insertTime'] = insertTime
                    rd['urls'] = thirdPicUris
                    self.pic001maoInfo.insert(rd)
                    if not os.path.exists(thirdPicDesc):
                        os.system('mkdir -p %s' % thirdPicDesc)
                    for thirdPicUri in thirdPicUris:
                        print(thirdPicUri)
                        name = thirdPicUri.split('/')[-1].strip()
                        f = os.path.join(thirdPicDesc, name)
                        self.logCrawPic(thirdPicUri, {}, f)
                        # break
                    self.num += 1
                    # break
            # break


    def classUriGen(self, classUri):
        '''
        根据第一个classUri首页生成其他连接
        :return:
        '''
        # 获取该类pic的总页数
        r = self.get(classUri, {}, total=10).text  # 不要代理
        if r == False:
            return []
        e = etree.HTML(r)
        totalS = e.xpath('//div[@class="pagination"]')[0].text
        total = totalS.split('/')[1].replace(u'页', '')
        # 生成该类小说的页面链接
        classUris = []
        classBase = classUri[:-6]
        for i in range(1, int(total)):
            classUri = classBase+str(i)+'.html'
            classUris.append(classUri)
        return classUris


    def crawlRun(self):
        self.engin()



if __name__ == '__main__':
    craw001maoPic = Craw001maoPic()
    craw001maoPic.crawlRun()