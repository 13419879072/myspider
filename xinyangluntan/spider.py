import requests
import re
from lxml import etree
import time
import random
import pymongo
from datetime import datetime

class XyluntanSpider:
    def __init__(self):
        self.star_url = "http://bbs.0376.net/search.php?mod=forum&searchid=1&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%E8%BF%9D%E6%B3%95"
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
        page_url = self.star_url
        while True:
            content = self.parse_url(page_url)
            html = etree.HTML(content)

            lis = html.xpath('//li[@class="pbw"]/h3/a')

            for li in lis:
                item = {}
                item['title'] = "".join(li.xpath('.//text()'))  #标题
                item['href'] = "".join(li.xpath('./@href')) #链接

                content2 = self.parse_url(item['href'])
                html2 = etree.HTML(content2)

                time = "".join(html2.xpath('//*[@id="postlist"]/div[1]/div/div/span[1]//text()'))

                item['post_time'] = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')  #时间
                item['user_name'] = "".join(html2.xpath('//*[@id="postlist"]/div[1]/div/div/a[1]//text()')) #发表人
                item['detail'] = "".join(html2.xpath('//table[@class="plhin nthread_firstpost"]/tr[1]//text()')).replace('\r\n','').replace('.pcb{margin-right:0} ','') #内容
                item['detail_img'] = [] #内容图片链接
                detail_img = html2.xpath('//table[@class="plhin nthread_firstpost"]/tr[1]//img/@src')
                for img in detail_img:
                    if img.startswith('http://bbs.0376.net/'):
                        item['detail_img'].append(img)
                    else:
                        item['detail_img'].append('http://bbs.0376.net/'+img)

                item['look_num'] = "".join(re.findall(r'浏览:&nbsp;&nbsp;(.*?)</span>',content2)) #浏览数
                item['reply_num'] = "".join(re.findall(r'回复:&nbsp;&nbsp;(.*?)</span>',content2)) #回复数

                item['detail_detail'] = []
                divs = html2.xpath('//div[@class="nthread_postbox"]')

                for div in divs:
                    dic = {}
                    dic['detail_num'] = "".join(div.xpath('.//div[@class="pi"]/strong/a//text()')).replace('\r\n', '')  # 楼层
                    dic['detail_uname'] = "".join(div.xpath('.//div[@class="authi"]/a[1]//text()'))  # 用户名
                    dic['detail_time'] = "".join(div.xpath('.//div[@class="authi"]/em//text()')).replace('发表于 ', '')  # 时间
                    dic['detail_content'] = "".join(div.xpath('.//div[@class="pct"]//text()')).replace('\r\n', '')  # 内容

                    item['detail_detail'].append(dic)

                print(item)
                break

            nex_page = "".join(html.xpath('//a[@class="nxt"]/@href'))
            if nex_page == '':
                break
            else:
                page_url = 'http://bbs.0376.net/' + nex_page

            if input("是否继续(yes/no)") == "no":
                print(page_url)
                break



if __name__ == '__main__':
    spider = XyluntanSpider()
    spider.run()
