import requests
import pymongo
import re
from lxml import etree
import time
from datetime import datetime


class JinanSpider:
    def __init__(self):
        self.client = pymongo.MongoClient("192.168.1.170", 27017)["jinan"]["jinanitem"]
        self.startrecord = 1  # +30
        self.endrecord = 30  # +30 如果为空响应dataStore = [];
        self.page_url = 'http://mslx.jinan.gov.cn/lm/front/mailpublist_dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=10' % (str(self.startrecord), str(self.endrecord))
        self.data = {       #三个机构post提交的参数不一样，url一样
            'sysid': '001',
            'month': '0',
            'sess': '0',
            'vc_parentid': '0072',
            'vc_targetgroup_not': '0003',
            'vc_ftlname': 'mailfeedback.ftl',
            'mailstate': '1',
            'orderfield': '2',
        }
        self.headers = {
            'Referer': 'http://mslx.jinan.gov.cn/lm/front/mailfeedback.jsp?sysid=001&editpagename=mailfeedback02.htm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }

    def post_content(self, url):
        resp = requests.post(url=url, data=self.data, headers=self.headers)
        time.sleep(1)
        content = resp.content.decode('utf-8', 'ignore')
        return content

    def get_html(self, url):
        resp = requests.get(url=url, headers=self.headers)  # 响应可以正常获取，但解码后数据没有了，只能写到本地再读出来
        with open('./content.html', 'wb')as file1:
            file1.write(resp.content)
        time.sleep(1)
        with open('./content.html', 'r', encoding='utf8')as file2:
            content = file2.read()
        time.sleep(1)
        html = etree.HTML(content)
        return html

    def save_mongo(self,item):
        if self.client.find_one({"number":item["number"]}):
            print("重复数据:%s"%item)
        else:
            self.client.insert(item)
    def run(self):
        while True:
            content = self.post_content(self.page_url)
            self.startrecord += 30
            self.endrecord += 30
            self.page_url = 'http://mslx.jinan.gov.cn/lm/front/mailpublist_dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=10' % (str(self.startrecord), str(self.endrecord))

            if content == "dataStore = [];":
                break
            numbers = re.findall(r"class='font12'> (.*?)</td>	<td", content)
            titles = re.findall(r"点击标题查看详细信息' target='_blank'>(.*?)</a>", content)
            types = re.findall(
                r"<td align='center' width='76' class='font12' height=35 > (.*?)</td>	<td align='center'", content)
            departments = re.findall(r'height=35 >([\u4e00-\u9fa5]+?)</td>	 </tr>","<tr>', content)
            hrefs = re.findall(r"<a href='(.*?)' title='点击标题查看详细信息'", content)
            print(self.startrecord)

            for i in range(30):
                item = {}
                item['number'] = numbers[i]  # 邮件编号
                item['title'] = titles[i]  # 邮件标题
                item['type'] = types[i]  # 类型
                item['department'] = departments[i]  # 受理部门
                item['href'] = 'http://mslx.jinan.gov.cn/lm/front/' + hrefs[i]  # 邮件链接

                html = self.get_html(item['href'])

                item['name'] = "".join(html.xpath('//table[@class="viewform"]/tr[2]/td[2]//text()')).replace('\xa0',
                                                                                                             '')  # 名字

                submit_time = "".join(html.xpath('//table[@class="viewform"]/tr[2]/td[4]//text()')).replace('\xa0',
                                                                                                            '')  # 提交时间
                item['submit_time'] = datetime.strptime(submit_time, '%Y-%m-%d %H:%M:%S')

                item['submit_detail'] = "".join(html.xpath('//table[@class="viewform"]/tr[4]/td[2]//text()')).replace(
                    '\xa0', '').replace(' ', '').replace('\n', '')  # 提交内容
                item['status'] = "".join(html.xpath('//table[@class="viewform"]/tr[8]/td[2]//text()')).replace('\xa0',
                                                                                                               '')  # 处理状态
                item['answer_detail'] = "".join(html.xpath('//table[@class="viewform"]/tr[10]/td[2]//text()')).replace(
                    '\xa0', '').replace(' ', '').replace('\n', '')  # 回复内容

                answer_time = "".join(html.xpath('//table[@class="viewform"]/tr[11]/td[4]//text()')).replace('\xa0',
                                                                                                             '')  # 回复时间
                item['answer_time'] = datetime.strptime(answer_time, '%Y-%m-%d %H:%M:%S')

                item['satisfaction'] = "".join(html.xpath('//table[@class="viewform"]/tr[12]/td[2]//text()')).replace(
                    '\xa0', '')  # 满意度

                print(item)

            if input('是否继续（yes/no）') == 'no':
                break


if __name__ == '__main__':
    spider = JinanSpider()
    spider.run()
