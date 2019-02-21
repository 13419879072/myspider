# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hmting.items import *
from datetime import datetime
import re


class HmtingspiderSpider(CrawlSpider):
    name = 'hmtingspider'
    allowed_domains = ['www.hmting.com']
    start_urls = [
        'http://www.hmting.com/search.php?mod=forum&searchid=140&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%BB%B7%BE%B3%CE%DB%C8%BE']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="nxt"]',)), follow=True),  # 自动找到下一页的地址并发送请求
        Rule(LinkExtractor(restrict_xpaths=('//h3[@class="xs3"]/a',)), callback='parse_item'),  # 向每一个帖子发送请求
    )

    def parse_item(self, response):
        item = HmtingItem()
        item["href"] = response.request.url  # 帖子链接
        item['title'] = response.xpath('//span[@id="thread_subject"]/text()').extract_first()  # 标题
        item['look_num'] = response.xpath('//span[@class="xi1"][1]/text()').extract_first()  # 查看数
        item['reply_num'] = response.xpath('//span[@class="xi1"][2]/text()').extract_first()  # 回复数
        item['category'] = response.xpath('//div[@id="pt"]/div/a[4]/text()').extract_first()  # 帖子类别

        floors = response.xpath('//div[@id="postlist"]/div/table')  # 所有楼层

        item['detail'] = []
        for floor in floors:
            dic = {}

            detail_num = floor.xpath('.//div[@class="pi"]/strong//text()').extract()
            dic['detail_num'] = re.sub(r'[\r\n\s]*', "", "".join(detail_num))  # 楼层数

            detail_time1 = floor.xpath('.//div[@class="pti"]/div[@class="authi"]/em/text()').extract_first()  # 该楼层发表时间
            detail_time2 = '20' + detail_time1.replace('发表于 ', '')
            dic['detail_time'] = datetime.strptime(detail_time2, '%Y-%m-%d %H:%M')

            detail_name = floor.xpath('.//a[@class="xw1"]/text()').extract_first()  # 该楼层用户名字
            dic['detail_name'] = detail_name
            try:
                detail1 = floor.xpath('.//div[@class="pcb"]//text()').extract()
                detail2 = "".join(detail1)
                detail3 = re.sub(r'[\\r\\n\s]', '', detail2)
                dic['detail_detail'] = re.sub(r'来自:.*', '', detail3)  # 帖子详情
                dic['detail_from'] = "".join(re.findall(r'来自:(.*)', detail3))  # 来自哪个客户端
            except:
                dic['detail_detail'] = ''

            try:
                dic['detail_img'] = floor.xpath('.//div[@class="pcb"]//img/@file').extract()  # 帖子中图片链接
            except:
                dic['detail_img'] = []

            item['detail'].append(dic)

        item['post_time'] = item['detail'][0]['detail_time']
        item['user_name'] = item['detail'][0]['detail_name']

        print(item)
        # yield item