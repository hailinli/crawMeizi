# -*- coding: utf-8 -*-

__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'
import requests
import re
import pymongo
import random



class Proxy:

    def __init__(self):

        # 免费代理ip网站
        self.proxyIpUriParam = {
            'getnum': 10000,
            'anonymoustype': 3,
            'proxytype': 2,
            'api': '66ip'
        }
        self.proxyIpUri = 'http://www.66ip.cn/nmtq.php'
        self.header = {
            'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",

        }
        self.proxys = []

        connection = pymongo.MongoClient()
        tdb = connection.crawJiandan
        self.proxyUsefuls = tdb.proxy
        self.tmpUsefulProxy = []


    def _getFreeProxyIp(self):
        '''
        获得免费的代理ip
        :param q:
        :return:
        '''
        r = requests.get(self.proxyIpUri, params=self.proxyIpUriParam)
        html = r.text
        ipZz = r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]):\d{2,5}'
        reIp = re.compile(ipZz)
        self.proxys = reIp.findall(html)


    def _check(self, proxy):
        '''
        取得可用代理ip
        :param proxy:
        :return:
        '''
        try:
            proxies = {
                "http": "http://%s" % proxy,
                "https": "http://%s" % proxy
            }
            r = requests.get('http://jandan.net/', proxies=proxies,  headers = self.header)
            if r.ok:
                print('%s is ok' % proxy)
                self.proxyUsefuls.insert({'proxy': proxy})
        except Exception as e:
            pass


    def _cheakAll(self):
        '''
        取得所有可用的代理ip
        :return:
        '''
        for proxy in self.proxys:
            # print(proxy)
            self._check(proxy)


    def genProxyUsefuls(self):
        self._getFreeProxyIp()
        self._cheakAll()


    def getOneProxy(self):
        '''
        随机从数据库代理池里获取一条数据,并更新临时代理池
        :return:
        '''
        allProxy = list(self.proxyUsefuls.find())
        self.tmpUsefulProxy = allProxy
        # print(self.tmpUsefulProxy)
        return random.choice(allProxy)['proxy']


    def getTmpOneProxy(self):
        '''
        随机从临时代理池里获取一条数据
        :return:
        '''
        return random.choice(self.tmpUsefulProxy)['proxy']


if __name__ == '__main__':
    proxy = Proxy()
    proxy.genOneProxy()