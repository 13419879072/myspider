import requests
from lxml import etree
import time
import random
import re
from datetime import datetime
import pymongo



class JyzufangSpider:
    def __init__(self):
        self.url = 'http://www.jy510.com/erent-page-1.html'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }
        self.client = pymongo.MongoClient("39.165.96.15", 27017)["jiangyinzufang"]["zufangitem"]

    def get_content(self, url):
        resp = requests.get(url=url, headers=self.headers)
        time.sleep(2)
        content = resp.content.decode('gbk', 'ignore')
        return content

    def get_html(self, content):
        html = etree.HTML(content)
        return html

    def save_mongo(self,item):
        if self.client.find_one({"number":item["number"]}):
            print("重复数据:%s"%item)
        else:
            self.client.insert(item)

    def run(self):
        while True:
            content = self.get_content(self.url)
            html = self.get_html(content)
            ul_list = html.xpath('//ul[@class="cl"]')
            for ul in ul_list:
                try:
                    item = {}
                    href = ul.xpath('./li[1]/a/@href')[0]
                    item['href'] = 'http://www.jy510.com/' + href   #链接
                    if self.client.find_one({"href": item["href"]}):
                        print('数据重复：%s'%item['href'])
                        continue
                    item['title'] = "".join(ul.xpath('./li[1]/a/@title')) #标题
                    item['acreage'] = "".join(ul.xpath('./li[2]//text()')) #面积
                    item['floor_num'] = "".join(ul.xpath('./li[3]//text()')) #楼层
                    item['money'] = "".join(ul.xpath('./li[4]//text()')).replace('\r','').replace('\n','').replace('\t','') #价格
                    item['house_type'] = "".join(ul.xpath('./li[5]//text()')) #户型
                    item['fitment'] = "".join(ul.xpath('./li[6]//text()')) #装修

                    content2 = self.get_content(item['href'])
                    html2 = self.get_html(content2)

                    item['number'] = "".join(re.findall(r'房源编号：(.*?) &nbsp',content2))  #房源编号

                    update_time = "".join(re.findall(r'发布时间：(.*?)\(',content2)) #发布时间
                    item['update_time'] = datetime.strptime(update_time,'%Y-%m-%d')

                    item['area'] = "".join(html2.xpath('//div[@class="detail-r"]/p[@class="detail-one"][1]/span[2]/a[1]/text()')) #小区
                    item['site'] = "".join(html2.xpath('//div[@class="detail-r"]/p[@class="detail-one"][2]/span[1]/text()')) #地址
                    item['facility'] = "".join(html2.xpath('//p[@class="infos"][3]/text()')) #配套设施

                    img_rls = html2.xpath('//ul[@id="imgList"]//img/@src') #图片
                    item['img_rl'] = []
                    if img_rls != '':
                        for img_rl in img_rls:
                            item['img_rl'].append('http://www.jy510.com/' + img_rl)
                    item['phone'] = "".join(re.findall(r'>拨打：(.*?)</span>',content2))
                    item['let_way'] = ''    #出租方式，此网站没有
                    item['orientation'] = ''    #朝向，此网站没有
                    item['live_time'] = ''    #入住时间，此网站没有
                except:
                    continue
                print(item)
                self.save_mongo(item)
            next_page = "".join(html.xpath('//a[@class="next"]/@href'))
            if next_page == '':
                break
            else:
                next_url = 'http://www.jy510.com/' + next_page
                self.url = next_url
            if input('是否继续（yes/no）') == 'no':
                print(next_page)
                break



if __name__ == '__main__':
    jy = JyzufangSpider()
    jy.run()
