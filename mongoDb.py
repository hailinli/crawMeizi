# -*- coding: utf-8-*-

__author__ = 'lihailin'
__email__ = '1501210931@qq.com'
__date__ = '2018年5月10日'

import pymongo
import log
import logging
log.initLogConf()
logg = logging.getLogger(__file__)

class MongoDbOpreater:

    def __init__(self, db, table):
        self.connection = pymongo.MongoClient('localhost', 27017)    #获取的连接
        self.db = self.connection[db]        #创建数据库db
        self.tableOP = self.db[table]    #创建或者选择要操作的集合


    def insert(self, data):
        """
        向数据库中插入指定的数据
        :param data: dict, 要插入的数据，这里的是字典的类型比如：{"name":"chenjiabing","age":22}
        :return: 插入成功返回True,反之返回false
        """
        try:
            self.tableOP.insert(data)
            logging.info('数据插入成功: %s' % data)
            return True
        except:
            logging.warn('数据插入失败: %s' % data)
            return False

    #
    # def getTableOpreater(self):
    #     '''
    #     得到可直接操作的表
    #     :return:
    #     '''
    #     return self.tableOP
