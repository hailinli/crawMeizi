# -*- coding: utf-8-*-
__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'

import crawBase
import crawDi81
import crawMzitu
import craw001maoPic
import craw001maoXs

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

class Factory001maoPic:
    def __init__(self):
        pass

    def creat001maoPic(self):
        return craw001maoPic.Craw001maoPic()


class Factory001maoXs:
    def __init__(self):
        pass

    def creat001maoXs(self):
        return craw001maoXs.Craw001maoXs()
