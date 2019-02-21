import requests
import re
from lxml import etree
import time
import random
import pymongo
from datetime import datetime


class PengPaiSpider:
    def __init__(self):
        self.headers = {
            'referer': 'https://www.thepaper.cn/searchResult.jsp?inpsearch=%E7%8E%AF%E5%A2%83%E6%B1%A1%E6%9F%93',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }

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
        pageidx = 1
        while True:
            star_url = "https://www.thepaper.cn/load_search.jsp?k=%E7%8E%AF%E5%A2%83%E6%B1%A1%E6%9F%93&pagesize=10&searchPre=all_0:&orderType=1&pageidx={}".format(pageidx)
            content = self.parse_url(star_url)
            hrefs = re.findall(r'<h2><a href="(.*?)"',content)

            for i in hrefs:
                item = {}
                item['href'] = 'https://www.thepaper.cn/' + i   #链接
                content2 = self.parse_url(item['href'])
                html2 = etree.HTML(content2)

                item['title'] = "".join(html2.xpath('//h1[@class="news_title"]/text()'))    #标题
                item['user_name'] = "".join(html2.xpath('//div[@class="name"]/text()')).replace('\u200b','')  #发表人
                if item['user_name'] == "":
                    item['user_name'] = "".join(html2.xpath('//div[@class="news_about"]/p[1]/text()')).replace('\u200b','')
                    post_time = "".join(html2.xpath('//div[@class="news_about"]/p[2]/text()')).replace('\n','').replace('\t','').strip()  #时间
                else:
                    post_time = "".join(html2.xpath('//div[@class="news_about"]/p[1]/text()')).replace('\n', '').replace('\t', '').strip()  # 时间
                try:
                    item['post_time'] = datetime.strptime(post_time, '%Y-%m-%d %H:%M')
                except:
                    item['post_time'] = post_time

                item['detail'] = "".join(html2.xpath('//div[@class="news_txt"]//text()'))
                item['detail_img'] = html2.xpath('//div[@class="news_txt"]//img/@src')


                print(item)

            pageidx +=1
            if input("是否继续(yes/no)") == "no":
                print(star_url)
                break

if __name__ == '__main__':
    spider = PengPaiSpider()
    spider.run()


