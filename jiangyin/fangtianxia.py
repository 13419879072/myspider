import requests
from lxml import etree
import time
import random
import re
from datetime import datetime
import pymongo



class FtxSpider:
    def __init__(self):
        self.url = 'https://jy.zu.fang.com/'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'showAdnanjing=1; global_cookie=5gd8anqu0yvsgcmmc79hu4zrp19jqf1lw67; integratecover=1; zixun_fang_layed=1; city=jy; Captcha=49515A667A4D6F72784F507767794231496157336A666A6F67645A4C6D366767617A6E64554F4D44344B76585776363869436B706359496A756C3439337A344B663131776E4672704636343D; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_xag9acd6b1mffnqinydw933gn29jqfx061s*3; ASP.NET_SessionId=vylo1eexjihzn2owuxjsdx3f; __utma=147393320.2098877557.1546425154.1546426999.1546477888.3; __utmb=147393320.9.10.1546477888; __utmc=147393320; __utmz=147393320.1546426999.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'referer': 'https://jy.zu.fang.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }
        self.client = pymongo.MongoClient("jsaxd.tpddns.cn", 27017)["jiangyinzufang"]["zufangitem"]

    def get_content(self, url):
        resp = requests.get(url=url, headers=self.headers)
        time.sleep(2)
        content = resp.content.decode('gb2312', 'ignore')
        return content

    def get_html(self, content):
        html = etree.HTML(content)
        return html

    def save_mongo(self,item):
        if self.client.find_one({"href":item["href"]}):
            print("重复数据:%s"%item)
        else:
            self.client.insert(item)

    def run(self):
        content = self.get_content(self.url)
        html = self.get_html(content)
        while True:

            hrefs = html.xpath('//dd[@class="info rel"]/p[1]/a/@href')

            for href in hrefs:
                url = 'https://jy.zu.fang.com' + href
                i = 0
                while True:
                    content2 = self.get_content(url)
                    html2 = self.get_html(content2)

                    title = "".join(html2.xpath('//h1[@class="title"]/text()|//h1[@class="title "]/text()'))    #有的多了一个空格
                    if title == '':  # 有时候请求得不到正常响应
                        i += 1
                        if i > 3:
                            break
                        continue
                    else:
                        break
                if title == '':
                    continue
                else:
                    item = {}
                    item['href'] = url  #链接
                    item['title'] = title   #标题
                    number = "".join(html2.xpath('//span[@class="mr10"]/text()'))   #房源编号
                    item['number'] = number.replace('房源编号 ','')

                    update_time1 = "".join(html2.xpath('//p[@class="gray9 fybh-zf"]/span[2]/text()')) #时间
                    update_time2 = re.sub(r'更新时间 ','',update_time1)
                    item['update_time'] = datetime.strptime(update_time2, '%Y-%m-%d')   #转换成时间对象

                    money1 = "".join(html2.xpath('//div[@class="trl-item sty1"]//text()|//div[@class="trl-item sty1 rel"]//text()'))    #价格
                    money2 = money1.replace('\r\n','')
                    item['money'] = money2.replace(' ','')

                    item['let_way'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[1]//text()'))  #出租方式
                    item['house_type'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[2]/div[1]//text()'))   #户型
                    item['acreage'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[3]/div[1]//text()'))  #建筑面积
                    item['orientation'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[4]/div[1]/div[1]//text()'))  #朝向
                    item['floor_num'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[4]/div[2]/div[1]//text()'))  #楼层
                    item['fitment'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[4]/div[3]/div[1]//text()'))  #装修

                    item['facility'] = ",".join(html2.xpath('/html/body/div[5]/div[2]/div[1]/div[2]/div[2]/ul/li/text()|/html/body/div[5]/div[2]/div[1]/div[1]/div[2]/ul/li/text()'))  #配套设施

                    area1 = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[5]/div[1]/div[2]//text()'))  #小区
                    area2 = area1.replace(' ','')
                    area3 = area2.replace('\r\n','')
                    item['area'] = area3

                    item['site'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[5]/div[2]/div[2]/a//text()'))  #地址

                    item['live_time'] = "".join(html2.xpath('/html/body/div[5]/div[1]/div[2]/div[5]/div[3]/div[2]/span//text()'))  #入住时间，有的为空
                    item['img_rl'] = html2.xpath('/html/body/div[5]/div[2]/div[1]/div[2]/div[2]//img/@src|/html/body/div[5]/div[2]/div[1]/div[3]/div[2]//img/@src')  #图片
                    item['phone'] = "".join(html2.xpath('//p[@class="text_phone"]/text()|//div[@class="tjcont-jjr-line2 clearfix"]/text()')).replace(' ','').replace('\n','').replace('\r','')   #联系方式
                    print(item)
                    self.save_mongo(item)

            next_page = "".join(html.xpath('//*[@id="rentid_D10_01"]/a[contains(text(),"下一页")]/@href')) #下一页地址
            if next_page == '':
                break
            else:
                next_url = 'https://jy.zu.fang.com/' + next_page
                content = self.get_content(next_url)
                html = self.get_html(content)



if __name__ == '__main__':
    ftx = FtxSpider()
    ftx.run()
