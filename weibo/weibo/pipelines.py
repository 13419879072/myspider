# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem #可抛出异常
import logging

class WeiboPipeline_Duplicates(object):
    '''去重'''
    def open_spider(self,spider):
        self.client = pymongo.MongoClient("39.165.96.15", 27017)["weibo"]["WeiboItem"]

    def process_item(self, item, spider):
        # if self.client.find_one(dict(item)):  #按所有数据重复查重
        if self.client.find_one({"href":item["href"]}):  #按该条微博地址查重
            #抛出异常，管道传递结束。如果不这样写，管道会继续往下传递
            raise DropItem("重复数据:%s"%item)
        else:
            return item
        # self.client.delete_one({"href": item["href"]})  # 如果有重复数据就删除原来的然后更新
        # self.client.insert(item)

class WeiboPipeline_Mongo(object):
    '''插入数据库'''
    def open_spider(self,spider):
        self.client = pymongo.MongoClient("39.165.96.15", 27017)["weibo"]["WeiboItem"]  # 配置数据库

    def process_item(self, item, spider):
        self.client.insert(dict(item))  # 转成字典传到数据库
        return item
