import requests
from lxml import etree
import re


headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
}
url = 'https://baike.baidu.com/item/%E6%9D%A8%E5%B9%82?qq-pf-to=pcqq.group'

resp = requests.get(url=url,headers=headers2)
content = resp.content.decode('utf-8','ignore')
with open('./baike.html','w')as file:
    file.write(content)


