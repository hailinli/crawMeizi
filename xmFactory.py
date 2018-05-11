# -*- coding: utf-8-*-
__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'

import crawBase
import crawDi81
import  crawMzitu

class FactoryBase:
    def __init__(self):
        pass


class FactoryDi81:
    def __init__(self):
        pass

    def creatDi81(self):
        return crawDi81.CrawDi81()

class FactoryMzitu:
    def __init__(self):
        pass

    def creatMzitu(self):
        return crawMzitu.CrawMzitu()
