import requests
import re
import json
from lxml import etree
import time
import random
import pymongo
from ploar import ploar




'''
tieba-tiebaitem  数据库-表
_id         数据id
title       帖子标题
href        帖子链接
user_name   发帖人名字
reply_num   帖子回复数
tb_age      发帖人吧龄
post_num    发帖人的发帖数
post_time   发帖时间
data_from   来源
detail      帖子所有楼的详情
[
    detail_num      楼层
    detail_time     时间
    detail_from     来自
    detail_uname    名字
    detail_level    等级    
    detail_detail   内容
    detail_img      图片 
    detail_video    视频
    detail_reply    回复
    detail_replynum 回复数
]
'''

'''
datas-data  数据库名-表名
_id         数据id(和另一个表id一致)
data_time   时间
data_title  主题
data_from   来源
data_user   用户名
'''

class TiebaSpider:
    def __init__(self, kw):
        self.kw = kw
        self.page_url = "http://tieba.baidu.com/f?kw={}&pn=1".format(self.kw) #食品安全2200  环境污染完结
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "BAIDUID=F95F3EA73899E7B6F2F24CD1036556B2:FG=1; BIDUPSID=F95F3EA73899E7B6F2F24CD1036556B2; PSTM=1548319382; TIEBA_USERTYPE=e69cb2e17038768719076425; BDUSS=51SWJud35obEd0TmxleUthNVEtTGVwS2t6fnNVVjdWVkM5R1VmM3BnN3haSEpjQUFBQUFBJCQAAAAAAAAAAAEAAADDs~lFnkXH6bXEtLrM7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPHXSlzx10pceG; STOKEN=ad102300d56a8ae67477d8d62eb7f256287933380c3ed93fa46a63885331de4e; TIEBAUID=631700b06ca314238700130f; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1457_21112_20880_28328_28413; 1173992387_FRSVideoUploadTip=1; bdshare_firstime=1548639482951; wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1548384134,1548385465,1548639442; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1548640059; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1548639483; Hm_lpvt_287705c8d9e2073d13275b18dbd746dc=1548640059",
        }
        self.client = pymongo.MongoClient("39.165.96.15", 27017)

    def parse_url(self, url):
        '''发送请求'''
        time.sleep(random.random())  # 每次发送请求停顿0-1s避免被封
        # print(url)
        resp = requests.get(url=url, headers=self.headers)
        return resp.content

    def parse_html(self, content):
        '''获取正确的content'''
        content = re.sub(r"<script>.*?</script>", r"", content, flags=re.DOTALL)  # 去掉所有js标签
        content = re.sub(r"<!--", r"", content)
        content = re.sub(r"-->", r"", content)  # 去掉注释
        return content

    def get_xpath(self, html_content, xpath_str):
        '''转换成html'''
        html = etree.HTML(html_content)
        return html.xpath(xpath_str)

    def save_mongo(self,tiebas,dataitem):
        '''保存到数据库'''
        tieba = self.client.tieba
        tiebaitem = tieba.tiebaitem
        # tiebaitem.delete_one({"href": tiebas["href"]})  #数据更新
        # tiebaitem.insert(tiebas)

        datas = self.client.datas
        data = datas.data
        # data.delete_one({"_id": dataitem["_id"]})
        # data.insert(dataitem)

        if tiebaitem.find_one({"href":tiebas["href"]}):  #按该条帖子地址查重
            print("重复数据:%s"%tiebas)
        else:
            tiebaitem.insert(tiebas)  # 存到到数据库
            data.insert(dataitem)  # 存到数据库


    def run(self):
        '''主函数'''
        while True:  # 该贴吧的每一页
            html_content = self.parse_html(self.parse_url(self.page_url).decode("utf-8"))  # 页面主要结构被js注释掉了
            # //li[@class=" j_thread_list thread_top j_thread_list clearfix"] 置顶的帖子
            tiezis = self.get_xpath(html_content, '//li[@class=" j_thread_list clearfix"]|//li[@class=" j_thread_list thread_top j_thread_list clearfix"]')  # 该页所有帖子

            for tiezi in tiezis:  # 该页的所有帖子
                tieba = {}
                data = {}

                data["data_study"] = 0  # 是否研判，预留字段
                data["data_chioce"] = 0  # 是否有效，预留字段
                import datetime
                data["data_time2"] = datetime.datetime(1970, 1, 1)  # 时间类型，预留字段
                data["data_beiyong1"] = ''  # 字符串，预留字段
                data["data_beiyong2"] = ''  # 字符串，预留字段
                data["data_beiyong3"] = ''  # 字符串，预留字段

                tieba["data_from"] = '百度贴吧'
                data["data_from"] = 1  #来源于贴吧用1

                tieba["detail"] = []

                tieba["title"] = tiezi.xpath('.//a[@class="j_th_tit "]/text()')[0]  # 帖子标题
                data["data_title"] = tieba["title"]

                emotion = ploar.run(tieba["title"]) #情感分析

                tieba["emotion"] = emotion
                data["data_emotion"] = emotion  # 1是正面 -1是负面 0是中性

                tieba["href"] = "https://tieba.baidu.com" + tiezi.xpath('.//a[@class="j_th_tit "]/@href')[0]  # 帖子地址
                if self.client.tieba.tiebaitem.find_one({"href":tieba["href"]}):    #直接判断url是否重复，若重复就不进行下面的操作
                    print('数据重复：%s'%tieba["href"])
                    continue

                data["data_href"] = tieba["href"]

                tieba["_id"] = "".join(re.findall(r'p/(.*)',tieba["href"])) #数据在数据库中的id
                data["_id"] = "".join(re.findall(r'p/(.*)',tieba["href"]))

                username = tiezi.xpath(
                    './/span[@class="tb_icon_author "]/@title|.//span[@class="tb_icon_author no_icon_author"]/@title')[
                    0]  # 会员和普通人名字不一样
                user_name = re.findall(r'主题作者: (.*)', username)[0]
                tieba["user_name"] = user_name  # 发帖人名字
                data["data_user"] = user_name  # 发帖人名字

                tieba["reply_num"] = tiezi.xpath('.//span[@title="回复"]/text()')[0]  # 回复数
                if tieba["reply_num"] == None:
                    tieba["reply_num"] = '0'

                uns = "".join(tiezi.xpath('.//span[@class="frs-author-name-wrap"]/a[@rel="noreferrer"]/@href'))   #获得un拼接发帖人详细信息
                if uns !='':
                    user_url = 'http://tieba.baidu.com' + uns  # 发帖人详细信息的url
                    user_content = self.parse_url(user_url).decode("utf-8", "ignore")  # 获取响应

                    #被封号的就没有信息
                    tieba["tb_age"] = "".join(re.findall(r'吧龄:(.*?)<',user_content))  # 吧龄
                    tieba["post_num"] = "".join(re.findall(r'发贴:(.*?)<',user_content))  # 发帖数
                else:
                    tieba["tb_age"] = ""
                    tieba["post_num"] = ""

                href_page = 1
                href = tieba["href"] + '?pn=' + str(href_page)
                tid = re.findall('p/(.*?)\?pn', href)[0]  # 后面评论要用到


                html_content2 = self.parse_url(href).decode("utf-8", "ignore")  # 向该贴发送请求
                pattern = "".join(re.findall(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', html_content2, re.S)) # 总页数
                while True:  # 该帖的所有页

                    # details = self.get_xpath(html_content2,'//div[@class="l_post l_post_bright j_l_post clearfix  "]|//div[@class="l_post j_l_post l_post_bright  "]|//div[@class="l_post j_l_post l_post_bright noborder "]')  # 该页所有楼层,精品贴
                    details = self.get_xpath(html_content2,'//div[@class="l_post l_post_bright j_l_post clearfix  "]')  # 该页所有楼层

                    for detail in details:  # 每一楼
                        dic = {}
                        floor = "".join(detail.xpath('.//span[@class="tail-info"]//text()'))
                        names = detail.xpath('.//a[@class="p_author_name j_user_card"]/text()')  # 有些人被封号显示不出名字
                        if len(names) == 0:
                            name = ''
                        else:
                            name = names[0]
                        level = "".join(detail.xpath('.//div[@class="d_badge_lv"]/text()'))
                        detail_content = "".join(
                            detail.xpath('.//div[@class="d_post_content j_d_post_content "]//text()'))
                        detail_img = detail.xpath('.//div[@class="d_post_content j_d_post_content "]//img/@src')
                        detail_video = detail.xpath('.//div[@class="d_post_content j_d_post_content "]//@data-video')


                        dic['detail_num'] = "".join(re.findall(r'\d+楼',floor)) #楼层
                        detail_time = "".join(re.findall(r'楼(.*)',floor)) #时间
                        from datetime import datetime
                        dic['detail_time'] = datetime.strptime(detail_time, '%Y-%m-%d %H:%M')   #转换成时间对象
                        dic['detail_from'] = "".join(re.findall(r'来自(.*?)\d+楼',floor)) #来自
                        dic['detail_uname'] = name   #名字
                        dic['detail_level'] = level   #等级
                        dic['detail_detail'] = detail_content.strip()   #内容
                        dic['detail_img'] = detail_img   #图片
                        dic['detail_video'] = detail_video   #视频

                        data_fields = detail.xpath('.//div[@class="j_lzl_r p_reply"]/@data-field')  #该帖每一楼的回复数和每一楼的评论pid
                        if len(data_fields) == 0:
                            dic['detail_reply'] = []    #回复
                            dic['detail_replynum'] = '0'    #回复数
                        else:
                            pid = re.findall('"pid":(.*?),', data_fields[0])[0]  # pid,拼接评论的url
                            total_num = re.findall('"total_num":(.*?)}', data_fields[0])[0]  # 该楼回复数
                            dic['detail_replynum'] = total_num
                            if dic['detail_replynum'] == None:
                                dic['detail_replynum'] = '0'
                            reply_page = 1
                            reply_url = 'https://tieba.baidu.com/p/comment?tid=' + tid + '&pid=' + pid + '&pn=' + str(
                                reply_page)
                            reply = []
                            while True:  # 该楼所有回复
                                reply_content = self.parse_url(reply_url).decode('utf-8', 'ignore')
                                reply_divs = self.get_xpath(reply_content, '//div[@class="lzl_cnt"]')
                                for reply_div in reply_divs:
                                    reply_details = reply_div.xpath('.//text()')
                                    reply_detail = re.sub(r"[(回复)]", "", "".join(reply_details))
                                    reply.append(reply_detail)
                                nums = etree.HTML(reply_content).xpath('//p//a[last()]/@href')  # 获取最后一页链接
                                if len(nums) == 0:
                                    break  # 只有一页
                                else:
                                    num = re.findall(r'#(.*)', nums[0])[0]  # 最后一页页码
                                    if reply_page >= int(num):
                                        break
                                    else:
                                        reply_page += 1
                                        reply_url = 'https://tieba.baidu.com/p/comment?tid=' + tid + '&pid=' + pid + '&pn=' + str(
                                            reply_page) #下一页评论的Url

                            dic['detail_reply'] = reply
                            if dic['detail_reply'] == None:
                                dic['detail_reply'] = []

                        tieba['detail'].append(dic)
                    break   #测试，直接结束只要第一页，正式开始时注释掉

                    # if href_page >= int(pattern): #下一页，正式开始时取消注释
                    #     break
                    # else:
                    #     href_page += 1
                    #     href = tieba["href"] + '?pn=' + str(href_page)
                    #     html_content2 = self.parse_url(href).decode("utf-8", "ignore")
                try:
                    tieba["post_time"] = tieba["detail"][0]['detail_time']
                    data["data_time"] = tieba["post_time"]
                except:
                    continue    #帖子已被删除就会报错
                print(tieba)    #一个帖子的完整数据
                self.save_mongo(tieba,data)

            next_url = self.get_xpath(html_content, '//a[@class="next pagination-item "]/@href')  # 下一页的地址
            # break
            if next_url:                  #是否有下一页，开始爬时候注销
                self.page_url = "http:" + next_url[0]
            else:
                break

            if input("是否继续(yes/no)") == "no":
                print(next_url)
                break


if __name__ == '__main__':
    spider = TiebaSpider("环境污染")
    spider.run()
