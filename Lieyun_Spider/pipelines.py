# -*- coding: utf-8 -*-

import Lieyun_Spider.settings
import pymongo
import time
from scrapy.conf import settings


class LieyunPipeline(object):
    def __init__(self):
        # 链接数据库

        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话

        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄

        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert(postItem)  # 向数据库插入一条记录
