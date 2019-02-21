import requests
import pymongo
from lxml import etree
import time
import random
import re


class CompanySpider:
    def __init__(self):
        self.headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "guid=21d1c06e06ec4feb9a8c106316f7a9a9; adv=adsnew%3D0%26%7C%26adsnum%3D2004282%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fs%253Fwd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526rsv_spt%253D1%2526rsv_iqid%253D0xefc7a40800036212%2526issp%253D1%2526f%253D8%2526rsv_bp%253D0%2526rsv_idx%253D2%2526ie%253Dutf-8%2526tn%253D93153557_hao_pg%2526rsv_enter%253D1%2526rsv_sug3%253D5%2526rsv_sug1%253D3%2526rsv_sug7%253D100; _ujz=MTQ3NDc5MzE5MA%3D%3D; ps=needv%3D0; 51job=cuid%3D147479319%26%7C%26cusername%3Dpythonnnnn%26%7C%26cpassword%3D%26%7C%26cname%3D%25C1%25F5%25CD%25FE%26%7C%26cemail%3Dgodliuwei%2540163.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0tmhk3oIieDU%26%7C%26cconfirmkey%3Dgof9N%252FLf2tn4g%26%7C%26cresumeids%3D.01c8l32GMKcA%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DgoleEBtOUoefo%26%7C%26to%3D6f5aca12e80464ee2e2bc9d0d513a3a05c402516%26%7C%26; search=jobarea%7E%60090200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA1%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1547708419%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA000000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA1%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1547708390%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch2%7E%601%A1%FB%A1%FA070200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA1%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1547707723%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch3%7E%601%A1%FB%A1%FA070200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%C7%B0%B3%CC%CE%DE%D3%C7+-%B4%FA%D5%D0%C6%B8+-51Job%D5%D0%C6%B8%BB%E1%A1%FB%A1%FA1%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1547707686%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch4%7E%601%A1%FB%A1%FA020000%2C00%A1%FB%A1%FA020600%A1%FB%A1%FA0107%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1545129588%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lastvisit%3D020000%26%7C%26lowbrowser%3Dnot%26%7C%26lastlogindate%3D20190117%26%7C%26",
        }   #51job的header

        self.headers2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "UM_distinctid=1685ae79f9a8cb-0577f591d9de11-63151074-1fa400-1685ae79f9b4ed; _uab_collina=154771335612650660470172; saveFpTip=true; acw_tc=7ae1439a15477133581947659e048859d6f434fba0459be2019265d819; QCCSESSID=n77mosuqa8caqosume7nn80fg1; CNZZDATA1254842228=779831654-1547712621-https%253A%252F%252Fwww.baidu.com%252F%7C1547858657; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1547713356,1547774451,1547861395; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1547862890; zg_did=%7B%22did%22%3A%20%221685ae79fe9528-0a5afd3d1bed7-63151074-1fa400-1685ae79fea8a9%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201547861393696%2C%22updated%22%3A%201547862935941%2C%22info%22%3A%201547713355759%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22a2b17b007c70e7ee2ade88013fe3af27%22%7D",
        }   #企查查的header
        # self.client = pymongo.MongoClient("192.168.1.170", 27017)

    def get_job(self, url):
        '''发送get请求'''
        time.sleep(random.random())
        resp = requests.get(url=url, headers=self.headers1)
        content = resp.content.decode('gb2312', 'ignore')
        return etree.HTML(content)

    def get_qcc(self, url):
        '''发送get请求'''
        time.sleep(random.random())
        resp = requests.get(url=url, headers=self.headers2)
        content = resp.content.decode('utf-8', 'ignore')
        return etree.HTML(content)

    def run(self):
        page_url = "https://jobs.51job.com/all/p1/"  # 51第一页
        while True:
            html = self.get_job(page_url)

            infos = html.xpath('//p[@class="info"]/a/@href')  # 所有公司
            for info in infos:
                item = {}

                html2 = self.get_job(info)  # 51job的公司详情页
                name = html2.xpath('//span[@class="icon_det"]/@title|/html/body/div[2]/div[2]/div[2]/div/h1/@title')[
                    0].replace(
                    '营业执照：', '')  # 公司认证名字或者公司名

                qcc_url = 'https://www.qichacha.com/search?key=' + name  # 去企查查的链接
                html3 = self.get_qcc(qcc_url)  # 企查查搜索公司页面

                company_url = "".join(html3.xpath(
                    '//*[@id="searchlist"]/table/tbody/tr/td[2]/a/@href|//*[@id="search-result"]/tr[1]/td[3]/a/@href'))  # 该公司的详情页
                if company_url == "":
                    continue
                else:
                    qcc_url2 = "https://www.qichacha.com" + company_url

                    html4 = self.get_qcc(qcc_url2)

                    item['name'] = "".join(html4.xpath('//*[@id="company-top"]/div[2]/div[2]/div[1]/h1/text()'))  # 公司名
                    if item['name'] == '':
                        continue
                    item['href'] = qcc_url2  # 链接
                    item['address'] = "".join(
                        html4.xpath('//td[contains(text(),"企业地址：")]/following-sibling::td[1]/text()')).strip()  # 公司地址
                    item['register_money'] = "".join(
                        html4.xpath('//td[contains(text(),"注册资本：")]/following-sibling::td[1]/text()')).strip()  # 注册资本
                    item['reality_money'] = "".join(
                        html4.xpath('//td[contains(text(),"实缴资本：")]/following-sibling::td[1]/text()')).strip()  # 实缴资本
                    item['status'] = "".join(
                        html4.xpath('//td[contains(text(),"经营状态：")]/following-sibling::td[1]/text()')).strip()  # 经营状态
                    item['found_time'] = "".join(
                        html4.xpath('//td[contains(text(),"成立日期：")]/following-sibling::td[1]/text()')).strip()  # 成立日期  1999-08-25  所有时间都是这种格式
                    item['company_type'] = "".join(
                        html4.xpath('//td[contains(text(),"公司类型：")]/following-sibling::td[1]/text()')).strip()  # 公司类型
                    item['industry'] = "".join(
                        html4.xpath('//td[contains(text(),"所属行业：")]/following-sibling::td[1]/text()')).strip()  # 所属行业
                    item['verify_time'] = "".join(
                        html4.xpath('//td[contains(text(),"核准日期：")]/following-sibling::td[1]/text()')).strip()  # 核准日期
                    item['num_people'] = "".join(
                        html4.xpath('//td[contains(text(),"人员规模")]/following-sibling::td[1]/text()')).strip()  # 人员规模
                    item['operating_period'] = "".join(
                        html4.xpath('//td[contains(text(),"营业期限")]/following-sibling::td[1]/text()')).strip()  # 营业期限
                    item['business_scope'] = "".join(
                        html4.xpath('//td[contains(text(),"经营范围：")]/following-sibling::td[1]/text()')).strip()  # 经营范围

                    '''股东信息 一个列表，里面每条数据是一个股东信息：股东名字|持股比例|认缴出资额|认缴出资日期'''
                    rets1 = html4.xpath('//*[@id="Sockinfo"]//h3[@class="seo font-14"]//text()')    #所有股东名字
                    rets2 = html4.xpath('//*[@id="Sockinfo"]//td[@class="text-center"][1]//text()') #所有股东持股比例
                    rets3 = html4.xpath('//*[@id="Sockinfo"]//td[@class="text-center"][2]//text()') #所有股东认缴出资额(万元)
                    rets33 = [i for i in rets3[0::2]]
                    rets4 = html4.xpath('//*[@id="Sockinfo"]//td[@class="text-center"][3]//text()') #所有股东认缴出资日期

                    item['shareholder'] = []    #股东信息

                    for i in range(len(rets1)):
                        rett = rets1[i].replace('\n', '').replace(' ', '') + '|' + rets2[i].replace('\n', '').replace(
                            ' ', '') + '%' + '|' + rets33[i].replace('\n', '').replace(' ', '') + '万元' + '|' + rets4[
                                   i].replace('\n', '').replace(' ', '')
                        item['shareholder'].append(rett)    #股东名字，持股比例，认缴出资，出资日期

                    '''公司变更信息  一个列表，里面每条数据是一条变更记录：变更日期|变更项目|变更前|变更后'''
                    trs1 = html4.xpath('//*[@id="Changelist"]//tr/td[2]')  # 变更日期
                    trs2 = html4.xpath('//*[@id="Changelist"]//tr/td[3]')  # 变更项目
                    trs3 = html4.xpath('//*[@id="Changelist"]//tr/td[4]')  # 变更前
                    trs4 = html4.xpath('//*[@id="Changelist"]//tr/td[5]')  # 变更后


                    item['change_record'] = []  #变更记录
                    for i in range(len(trs1)):
                        tr1 = "".join(trs1[i].xpath('.//text()')).replace('\n', '').replace(' ', '')
                        tr2 = "".join(trs2[i].xpath('.//text()')).replace('\n', '').replace(' ', '')
                        tr3 = "".join(trs3[i].xpath('.//text()')).replace('\n', '').replace(' ', '')
                        tr4 = "".join(trs4[i].xpath('.//text()')).replace('\n', '').replace(' ', '')
                        tr = tr1 + '|' + tr2 + '|' + tr3 + '|' + tr4
                        item['change_record'].append(tr)

                print(item)
                break
            page_url = "".join(html.xpath('//li[@class="bk"][2]/a/@href'))
            if page_url == '':
                print('爬取完毕。。。')
                break
            elif input("是否继续(yes/no)") == "no":
                print("下一页地址：", page_url)
                break


if __name__ == '__main__':
    spider = CompanySpider()
    spider.run()
