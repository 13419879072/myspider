import requests
import re
from lxml import etree



# url = 'http://mslx.jinan.gov.cn/lm/front/mailpubdetail.jsp?vc_id=7a810dc0-a180-48ec-b26e-71cf46355416&sysid=001&sess=0'
# resp = requests.get(url=url)
# content = resp.content
# with open('./content.html','wb')as file:
#     file.write(content)


with open('./content.html','r',encoding='utf8')as file:
    content = file.read()

print(content)
print(type(content))


uname1 = re.findall(r'class="list_pd1">(.+?) </td>',content)
uname2 = re.findall(r'class="list_pd1">(.+?) </td>',content)
uname3 = re.findall(r'class="list_pd2">(.+?) </td>',content,re.DOTALL)
print(uname1)
print(uname2)
print(uname3)