import requests
import re
from lxml import etree
import time
import random
import pymongo
from datetime import datetime

class FengHuangSpider:
    def __init__(self):
        self.star_url = "https://search.ifeng.com/sofeng/search.action?q=%E6%B2%B3%E5%8D%97%E8%BF%9D%E6%B3%95&c=1&chel=&p=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }

        # self.client = pymongo.MongoClient("39.165.96.15", 27017)

    def parse_url(self, url):
        '''发送请求'''
        time.sleep(random.random())  # 每次发送请求停顿0-1s避免被封
        # print(url)
        resp = requests.get(url=url, headers=self.headers)
        return resp.content.decode('utf-8','ignore')

    def save_mongo(self,tiebas,dataitem):
        '''保存到数据库'''
        pass


    def run(self):
        '''主函数'''
        content = self.parse_url(self.star_url)
        html = etree.HTML(content)
        divs = html.xpath('//div[@class="searchResults"]')
        for div in divs:
            item = {}
            item['title'] = "".join(div.xpath('.//a//text()')).replace('\xa0','')
            item['href'] = "".join(div.xpath('.//a/@href'))
            post_time = "".join(div.xpath('.//p/font//text()'))
            print(post_time)
            post_time2 = "".join(re.findall(r'.*? (.+)',post_time))
            item['post_time'] = datetime.strptime(post_time2,'%Y-%m-%d %H:%M:%S')

            content2 = self.parse_url(item['href'])
            html2 = etree.HTML(content2)

            item['detail'] = "".join(html2.xpath('//div[@class="text-3zQ3cZD4"]//text()'))
            item['detail_img'] = html2.xpath('//div[@class="text-3zQ3cZD4"]//img/@src')

            print(item)




if __name__ == '__main__':
    spider = FengHuangSpider()
    spider.run()
