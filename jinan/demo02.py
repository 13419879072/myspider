import requests
import re
from lxml import etree
from datetime import datetime




with open('./content.html','r',encoding='utf8')as file:
    content = file.read()

html = etree.HTML(content)
item = {}

item['name'] = "".join(html.xpath('//table[@class="viewform"]/tr[2]/td[2]//text()')).replace('\xa0','')  #名字

submit_time = "".join(html.xpath('//table[@class="viewform"]/tr[2]/td[4]//text()')).replace('\xa0','')   #提交时间
item['submit_time'] = datetime.strptime(submit_time,'%Y-%m-%d %H:%M:%S')

item['submit_detail'] = "".join(html.xpath('//table[@class="viewform"]/tr[4]/td[2]//text()')).replace('\xa0','').replace(' ','').replace('\n','')      #提交内容
item['status'] = "".join(html.xpath('//table[@class="viewform"]/tr[8]/td[2]//text()')).replace('\xa0','')    #处理状态
item['answer_detail'] = "".join(html.xpath('//table[@class="viewform"]/tr[10]/td[2]//text()')).replace('\xa0','').replace(' ','').replace('\n','')    #回复内容

answer_time = "".join(html.xpath('//table[@class="viewform"]/tr[11]/td[4]//text()')).replace('\xa0','')   #回复时间
item['answer_time'] = datetime.strptime(answer_time,'%Y-%m-%d %H:%M:%S')

item['satisfaction'] = "".join(html.xpath('//table[@class="viewform"]/tr[12]/td[2]//text()')).replace('\xa0','')    #满意度

print(content)
print(item)