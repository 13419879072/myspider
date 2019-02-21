import requests
import re
from lxml import etree
import time
import random
import pymongo
from datetime import datetime
import json
from selenium import webdriver

class TtouTiaoSpider:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }
        self.driver = webdriver.PhantomJS()
        # self.client = pymongo.MongoClient("39.165.96.15", 27017)

    def parse_url(self, url):
        '''发送请求'''
        time.sleep(1)  # 每次发送请求停顿0-1s避免被封
        # print(url)
        resp = requests.get(url=url, headers=self.headers)
        return resp.content.decode('utf-8', 'ignore')

    def save_mongo(self, tiebas, dataitem):
        '''保存到数据库'''
        pass

    def run(self):
        '''主函数'''
        pageidx = 0
        while True:
            star_url = "https://www.toutiao.com/api/search/content/?aid=24&offset={}&format=json&keyword=%E4%BF%A1%E9%98%B3%E8%BF%9D%E6%B3%95&autoload=true&count=20&cur_tab=1&from=search_tab&pd=synthesis".format(pageidx)
            content = self.parse_url(star_url)

            datas = json.loads(content)['data']
            for data in datas:
                item = {}

                try:
                    item['title'] = data['title']   #标题
                    item['user_name'] = data['media_name']

                    group_id = data['group_id']
                    item['href'] = 'https://www.toutiao.com/'+'a'+group_id+'/'  #链接

                    post_time = data['datetime']

                    item['post_time'] = datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')

                    item['detail_img'] = []
                    image_list = data['image_list']
                    for img in image_list:
                        item['detail_img'].append(img['url'])

                    self.driver.get(item['href'])
                    content2 = self.driver.page_source
                    html2 = etree.HTML(content2)

                    item['detail'] = "".join(html2.xpath('//div[@class="article-content"]//text()'))

                    print(item)
                except:
                    continue

            pageidx +=20
            if input("是否继续(yes/no)") == "no":
                print(star_url)
                break

if __name__ == '__main__':
    spider = TtouTiaoSpider()
    spider.run()


