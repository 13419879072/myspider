# -*- coding: utf-8 -*-
import scrapy
from weibo.items import *
import re
from urllib import parse
import requests
import json
import time
import random
import datetime
import pymongo
import hashlib
import string
from urllib.parse import quote


class WeibospiderSpider(scrapy.Spider):

    name = 'weibospider'  # 爬虫名
    allowed_domains = ['weibo.com']  # 约束为此域名下的内容
    start_urls = ['https://s.weibo.com/weibo?q=%E6%B7%AE%E6%B2%B3%E9%9D%9E%E6%B3%95%E9%87%87%E7%A0%82&wvr=6&Refer=SWeibo_box']   #淮河非法13

    def parse(self, response):
        client = pymongo.MongoClient("39.165.96.15", 27017)["datas"]["data"]
        divs = response.xpath('//div[@class="card"]')  # 此页的微博
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "SINAGLOBAL=9694735719328.338.1548330976047; un=13419879072; wvr=6; YF-V5-G0=1312426fba7c62175794755e73312c7d; SSOLoginState=1548639029; SCF=AkpECi4_MDd_uQkRcbmnk1bkX-YW9R6qSm0hhT5Jb1S7GTwiVKUjavkfDYojeW7c-Wo4EftQSus8XfW48NrKMPg.; SUB=_2A25xSitlDeRhGeNG7lQV-CzMzzSIHXVSPhutrDV8PUNbmtBeLUzRkW9NS1aV2Tu61OjyoeRDFWZAqLObR7VaKn4m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWTN4dcC6kxwuih_AU50vEb5JpX5KMhUgL.Fo-RSKqX1hz7Shn2dJLoIpWFIPHbIPHbIP-_eK.RS050; SUHB=04Wu7UUVI8OggI; ALF=1580175028; YF-Page-G0=8fee13afa53da91ff99fc89cc7829b07; wb_view_log_5856482048=1920*10801; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5152871013303.65.1548639034230; ULV=1548639034248:5:5:1:5152871013303.65.1548639034230:1548474880952; Ugrow-G0=57484c7c1ded49566c905773d5d00f82",
        }
        next_page = "".join(response.xpath('//a[@class="next"]/@href').extract())

        for div in divs:
            item = WeiboItem()  # 实例化一个字典
            data = {}

            data["data_study"] = 0  #是否研判，预留字段
            data["data_chioce"] = 0  #是否有效，预留字段
            data["data_time2"] = datetime.datetime(1970,1,1)  #时间类型，预留字段
            data["data_beiyong1"] = ''  #字符串，预留字段
            data["data_beiyong2"] = ''  #字符串，预留字段
            data["data_beiyong3"] = ''  #字符串，预留字段

            item["name"] = div.xpath('.//div[@class="info"]//a[@class="name"]/@nick-name').extract_first()  # 用户名
            data["data_user"] = item["name"]

            item["data_from"] = '新浪微博'  #数据来源
            data["data_from"] = 0  #来源于新浪微博用0

            href = div.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/@href').extract_first()
            item["href"] = "https:"+href  # 单条微博的地址

            data["data_href"] = item["href"]
            if client.find_one({"data_href": data["data_href"]}):  # 直接判断url是否重复，若重复就不进行下面的操作
                print('数据重复：%s' % data["data_href"])
                continue

            resp = requests.get(url=item["href"], headers=headers)  #发送请求获取时间
            time.sleep(1) #停顿1s避免获取不到
            resp_content = resp.content.decode('utf-8', 'ignore')
            publish_times = re.findall(r'date=\\"(\d{13})\\"', resp_content)

            try:
                publish_time = int(publish_times[0])
                item["publish_time"] = datetime.datetime.fromtimestamp(publish_time/1000)   #发表时间
            except:
                item["publish_time"] = ''

            data["data_time"] = item["publish_time"]

            id = re.findall(r'//weibo.com/(.*?)/',item["href"])[0]  #获取个人信息所需要的id
            item = self.get_userInfo(item,id)   #获取个人信息

            come_from = div.xpath(
                'string(./div[@class="card-feed"]/div[@class="content"]/p[@class="from"])').extract_first()  # 时间和来自

            come_from1 = re.sub(r'[\\n\s]', '', come_from)
            item["come_from"] = re.sub(r'.*?来自','',come_from1)


            like = div.xpath('.//div[@class="card-act"]//a[@title]/em/text()').extract_first()
            if like == None:
                like = 0  # 没有点赞数的处理
            item["like"] = int(like)  # 点赞数

            transmit = div.xpath('.//div[@class="card-act"]//li[2]//text()').extract_first()
            if transmit == '转发 ':
                transmit = '转发 0'  # 没有人转发的处理
            item['transmit'] = transmit  # 转发数

            authentication = div.xpath('.//div[@class="info"]//a[@class="name"]/following-sibling::a[1]/@title').extract_first()

            if authentication == None:
                authentication = ''

            item['authentication'] = authentication

            comment_sum = div.xpath('.//div[@class="card-act"]//li[3]//text()').extract_first()
            if comment_sum == '评论 ':
                comment_sum = '评论 0'  # 没有人评论的处理
            item['comment_sum'] = comment_sum  # 评论数

            detail = div.xpath('string(.//p[@node-type="feed_list_content_full"])').extract_first().replace("收起全文d",
                                                                                                            "")  # 内容长不能直接显示的处理
            if detail == '':  # 内容短可以直接显示出来
                detail = div.xpath('string(.//p[@node-type="feed_list_content"])').extract_first()

            detail = re.sub(r"[\s(\u200b')]", '', detail)  # 去掉多余空格和字符
            item["detail"] = detail  # 微博内容

            emotion = self.run(detail)
            item["emotion"] = emotion   #1是正面 -1是负面 0是中性
            data["data_emotion"] = emotion   #1是正面 -1是负面 0是中性

            if len(detail) <= 25:
                data["data_title"] = detail
            else:
                data["data_title"] = detail[0:25] + "..."

            detail_image = div.xpath('.//div[@class="content"]/div[2]//img/@src').extract()  # 图片地址

            if len(detail_image) == 0:
                item["detail_image"] = ''
            else:
                item["detail_image"] = detail_image

            detail_datas = []  # 存放data
            detail_video = []  # 视频的地址

            data_urls = div.xpath('.//div[@class="content"]/div[2]//a/@action-data').extract_first()  # 视频地址被js隐藏加密混淆
            # detail_data = None
            if data_urls != None:
                detail_datas = re.findall(r'video_src=(.*?)&cover_img', data_urls)

            if len(detail_datas) > 0:  # 防止内容无视频时下标越界
                detail_data = detail_datas[0]

                detail_video = parse.unquote(detail_data)  # 解码encodeURIComponent
            if len(detail_video) == 0:
                item["detail_video"] = ''
            else:
                item["detail_video"] = detail_video

            mid = div.xpath('./parent::div/@mid').extract_first()  # 父节点的mid,用于拼接评论的Url

            item["_id"] = mid
            data["_id"] = mid   #数据的id


            item = self.get_comment(item, mid)  # 去获取评论

            self.save_data(client,data)
            yield item  #返回item对象进入管道存储数据


        if next_page == '':
            pass
        else:
            next_url = 'https://s.weibo.com' + next_page
            if input("是否继续(yes/no)") == "no":
                print(next_url)
            else:
                yield scrapy.Request(
                    url=next_url,
                    headers=headers,
                    callback=self.parse
                )

    def get_userInfo(self,item,id):
        '''获取微博信息'''
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        resp = requests.get(url=url)
        time.sleep(random.random())
        content = resp.content.decode('utf-8','ignore')
        data = json.loads(content)

        try:
            item['authentication_name'] = data['data']['userInfo']['verified_reason']  # 微博认证名
        except:
            item['authentication_name'] = '无微博认证'   #没有认证会报错，抛出异常手动赋值
        try:    #有时候会获取不到
            item['followers_count'] = data['data']['userInfo']['followers_count']  # 粉丝数
            item['description'] = data['data']['userInfo']['description']  # 简介
            item['urank'] = data['data']['userInfo']['urank']  # 微博等级
            item['follow_count'] = data['data']['userInfo']['follow_count']  # 关注
            item['profile_image_url'] = data['data']['userInfo']['profile_image_url']   #头像
        except:
            item['followers_count'] = 0  # 粉丝数
            item['description'] = ''  # 简介
            item['urank'] = 0  # 微博等级
            item['follow_count'] = 0  # 关注
            item['profile_image_url'] = ''  # 头像

        return item




    def get_comment(self, item, mid):
        '''获取评论'''
        url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=' + mid + '&page=' + '1' + '&filter=hot&filter_tips_before=0&from=singleWeiBo'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "SINAGLOBAL=9694735719328.338.1548330976047; un=13419879072; wvr=6; YF-V5-G0=1312426fba7c62175794755e73312c7d; SSOLoginState=1548639029; SCF=AkpECi4_MDd_uQkRcbmnk1bkX-YW9R6qSm0hhT5Jb1S7GTwiVKUjavkfDYojeW7c-Wo4EftQSus8XfW48NrKMPg.; SUB=_2A25xSitlDeRhGeNG7lQV-CzMzzSIHXVSPhutrDV8PUNbmtBeLUzRkW9NS1aV2Tu61OjyoeRDFWZAqLObR7VaKn4m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWTN4dcC6kxwuih_AU50vEb5JpX5KMhUgL.Fo-RSKqX1hz7Shn2dJLoIpWFIPHbIPHbIP-_eK.RS050; SUHB=04Wu7UUVI8OggI; ALF=1580175028; YF-Page-G0=8fee13afa53da91ff99fc89cc7829b07; wb_view_log_5856482048=1920*10801; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=5152871013303.65.1548639034230; ULV=1548639034248:5:5:1:5152871013303.65.1548639034230:1548474880952; Ugrow-G0=57484c7c1ded49566c905773d5d00f82",
        }

        # time.sleep(random.random())   #停顿0-1s避免被封
        resp = requests.get(url=url, headers=headers)

        content = resp.content.decode('utf-8', 'ignore')

        try:
            dic = json.loads(content)  # json转字典

            html = dic["data"]["html"]  # 拿到评论的数据

            ret = re.findall(r'usercard=\"id=\d*?\">(.*?)<.*?</a>：(.*?)\s*?</div>', html)  # 提取内容
            ret2 = re.findall(r'<div class=\"WB_from S_txt2\">(.*?)</div>',html)    #提取时间
            #'class=\"W_ficon ficon_praised S_txt2\">.*?</em><em>(.*?)</em>'    #赞的正则表达式
            #"https://weibo.cn/u/%d?filter=0&page=1"
            #"https://weibo.cn/u/5191041328?filter=0&page=1"

            ls = []
            for i in range(0,len(ret)):
                '''对每条数据进行清洗'''
                m = re.sub(r'<img[\w\W]*?/>', '', ':'.join(ret[i]))
                m2 = re.sub(r'<a[\w\W]*?</a>', '', m)+' '+ret2[i]

                if m2 not in ls:
                    ls.append(m2)

            item['comment'] = ls  # 评论的1页内容
        except:
            item['comment'] = ''
        print(item)
        return item
    def save_data(self,client,data):

        if client.find_one({"_id":data["_id"]}):  #按该条数据id
            print("重复数据:%s"%data)
        else:
            client.insert(data)  # 存到数据库

        # client.delete_one({"data_href":data["data_href"]})   #如果有重复数据就更新
        # client.insert(data)



    def curlmd5(self,src):
        m = hashlib.md5(src.encode('UTF-8'))
        # 将得到的MD5值所有字符转换成大写
        return m.hexdigest().upper()

    def get_params(self,plus_item):
        global params
        # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
        t = time.time()
        time_stamp = str(int(t))

        # 请求随机字符串，用于保证签名不可预测  
        nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        # 应用标志，这里修改成自己的id和key  
        app_id = '2110900827'
        app_key = 'Z6gIDhi8NUSW6dcl'
        params = {'app_id': app_id,
                  'text': plus_item,
                  'time_stamp': time_stamp,
                  'nonce_str': nonce_str,
                  }
        sign_before = ''
        # 要对key排序再拼接
        for key in sorted(params):
            # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
            sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
        # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
        sign_before += 'app_key={}'.format(app_key)
        # 对字符串sign_before进行MD5运算，得到接口请求签名  
        sign = self.curlmd5(sign_before)
        params['sign'] = sign
        return params

    def get_sentiments(self,comments):
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"
        comments = comments.encode('utf-8')
        payload = self.get_params(comments)
        r = requests.post(url, data=payload)
        return r.json()

    def run(self,ret):
        # len(ret)<=66才会正常响应，一个汉字占3个字节，上限200字节
        ret0 = ret[:66]
        data = self.get_sentiments(ret0)
        polar = data['data']['polar']
        return polar
