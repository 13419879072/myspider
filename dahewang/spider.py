import requests
import re
from lxml import etree
import time
import random
import pymongo
from ploar import ploar


class DaHeSpider:
    def __init__(self):
        self.star_url = "http://bbs.dahe.cn/search.php?mod=forum&searchid=5332&orderby=sphinx&ascdesc=desc&searchsubmit=yes&kw=%B7%C7%B7%A8"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }

        # self.client = pymongo.MongoClient("39.165.96.15", 27017)
        self.client = pymongo.MongoClient("jsaxd.tpddns.cn", 27017)

    def parse_url(self, url):
        '''发送请求'''
        time.sleep(1)  # 每次发送请求停顿0-1s避免被封
        # print(url)
        resp = requests.get(url=url, headers=self.headers)
        return resp.content.decode('gbk','ignore')

    def save_mongo(self,dahes,dataitem):
        '''保存到数据库'''
        dahe = self.client.dahe
        daheitem = dahe.daheitem

        datas = self.client.datas
        data = datas.data

        if daheitem.find_one({"href":dahes["href"]}):  #按该条帖子地址查重
            print("重复数据:%s"%dahes)
        else:
            daheitem.insert(dahes)  # 存到到数据库
            data.insert(dataitem)  # 存到数据库



    def run(self):
        '''主函数'''
        page_url = self.star_url
        while True:
            content = self.parse_url(page_url)
            html = etree.HTML(content)

            lis = html.xpath('//li[@class="pbw"]')

            for li in lis:
                item = {}
                data = {}

                item['_id'] = "".join(li.xpath('./@id'))
                data['_id'] = item['_id']

                data["data_study"] = 0  # 是否研判，预留字段
                data["data_chioce"] = 0  # 是否有效，预留字段
                import datetime
                data["data_time2"] = datetime.datetime(1970, 1, 1)  # 时间类型，预留字段
                data["data_beiyong1"] = ''  # 字符串，预留字段
                data["data_beiyong2"] = ''  # 字符串，预留字段
                data["data_beiyong3"] = ''  # 字符串，预留字段

                item['data_from'] = '大河网'    #来源
                data['data_from'] = 2   #来源大河网为2

                item['title'] = "".join(li.xpath('./h3/a//text()'))  #标题
                data["data_title"] = item['title']

                emotion = ploar.run_polar(item["title"]) #情感分析

                item["emotion"] = emotion
                data["data_emotion"] = emotion  # 1是正面 -1是负面 0是中性

                href = "".join(li.xpath('./h3/a/@href')) #链接
                item['href'] = 'http://bbs.dahe.cn/' + href


                post_time = "".join(li.xpath('./p[3]/span[1]//text()'))

                from datetime import datetime
                item['post_time'] = datetime.strptime(post_time, '%Y-%m-%d %H:%M')  # 时间
                data['data_time'] = item['post_time']

                item['detail'] = []

                content2 = self.parse_url(item['href'])
                html2 = etree.HTML(content2)

                divs = html2.xpath('//div/table[@class="plhin"]')
                for div in divs:
                    dic = {}
                    dic['detail_uname'] = "".join(div.xpath('.//div[@class="authi"]/a[@class="xw1"]//text()'))  #名字

                    detail_time = "".join(div.xpath('.//div[@class="authi"]/em//text()')).replace('发表于 ','')

                    try:
                        dic['detail_time'] = datetime.strptime(detail_time,'%Y-%m-%d %H:%M:%S')  #时间
                    except:
                        dic['detail_time'] = detail_time.replace('\xa0','')

                    dic['detail_from'] = "".join(div.xpath('.//span[@class="xg1"]//a//text()'))    #来自
                    dic['detail_num'] = "".join(div.xpath('.//div[@class="pi"]/strong//text()')).replace('\r\n','')    #楼层
                    dic['detail_detail'] = "".join(div.xpath('.//td[@class="t_f"]//text()')).replace('\r\n','').replace('\xa0','').replace('\u3000','')    #内容
                    dic['detail_img'] = div.xpath('.//td[@class="t_f"]//img/@file')    #图片

                    item['detail'].append(dic)

                data['data_user'] = item['detail'][0]['detail_uname']
                item['user_name'] = data['data_user']
                print(item)
                # print(data)
                self.save_mongo(item,data)
                # break

            nex_page = "".join(html.xpath('//a[@class="nxt"]/@href'))
            if nex_page == '':
                break
            else:
                page_url = 'http://bbs.dahe.cn/' + nex_page

            if input("是否继续(yes/no)") == "no":
                print(page_url)
                break


if __name__ == '__main__':
    spider = DaHeSpider()
    spider.run()
