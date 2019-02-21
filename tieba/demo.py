import requests
from lxml import  etree
url="https://mp.weixin.qq.com/s?__biz=MzAwNDI4ODcxNA==&mid=2652250971&idx=1&sn=89e611e7714c767f07f1d06b0e032428&chksm=80ccbafeb7bb33e86a51ca01e74878976b0f736849f03c40880dcb92247fe6ede60418faaaf1&scene=27#wechat_redirect"
r22 = requests.get(url=url)
content22 = etree.HTML(r22.text)
# 文章的全部内容
content = content22.xpath("//div[@id='js_content']//text()")

content1 = "".join(content)
content1.replace("\n","")


print(content1.strip())
