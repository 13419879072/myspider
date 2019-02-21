# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    _id = scrapy.Field()    #数据id
    name = scrapy.Field()  # 用户名
    href = scrapy.Field()  # 该条微博的地址
    detail = scrapy.Field()  # 内容，如果有位置信息是直接显示在内容上的
    detail_video = scrapy.Field()   #内容中视频链接
    detail_image = scrapy.Field()   #内容中图片链接
    like = scrapy.Field()  # 点赞数
    transmit = scrapy.Field()   #转发数
    comment_sum = scrapy.Field()    #评论数
    comment = scrapy.Field()  # 评论
    publish_time = scrapy.Field()   #发表时间
    come_from = scrapy.Field()   #来自
    authentication = scrapy.Field() #微博认证类型
    authentication_name = scrapy.Field()    #微博认证名
    followers_count = scrapy.Field()   #粉丝数
    description = scrapy.Field()  #简介
    urank = scrapy.Field()  #微博等级
    follow_count = scrapy.Field()   #关注
    profile_image_url = scrapy.Field()  #头像
    data_from = scrapy.Field()  #数据来源
    emotion = scrapy.Field()  #情感分析