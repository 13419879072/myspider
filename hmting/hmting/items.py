# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HmtingItem(scrapy.Item):
    href = scrapy.Field()       #帖子链接
    title = scrapy.Field()      #标题
    look_num = scrapy.Field()   #查看数
    reply_num = scrapy.Field()  #回复数
    category = scrapy.Field()  #帖子类别
    post_time = scrapy.Field()  # 发表时间
    user_name = scrapy.Field()  # 发表人
    detail = scrapy.Field()  #帖子详情

