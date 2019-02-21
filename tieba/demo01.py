import requests
import re
from lxml import etree



headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }

url = 'https://tieba.baidu.com/p/2612989431?pn=1'

tieba = {}
tieba['detail'] = {}
resp = requests.get(url=url,headers=headers)

content = resp.content.decode("utf-8","ignore")

pattern = re.findall(r'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',content,re.S)[0]   #总页数

html = etree.HTML(content)


details = html.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
for detail in details:
    floor = "".join(detail.xpath('.//span[@class="tail-info"]//text()'))
    names = detail.xpath('.//a[@class="p_author_name j_user_card"]/text()') #有些人被封号显示不出名字
    if len(names) == 0:
        name = ''
    else:
        name = names[0]
    level = detail.xpath('.//div[@class="d_badge_lv"]/text()')[0]
    detail_content = "".join(detail.xpath('.//div[@class="d_post_content j_d_post_content "]//text()'))
    detail_img = ",".join(detail.xpath('.//div[@class="d_post_content j_d_post_content "]//img/@src'))
    detail_video = ",".join(detail.xpath('.//div[@class="d_post_content j_d_post_content "]//@data-video'))

    tieba['detail']['floor'] = floor    #几楼什么时间
    tieba['detail']['name'] = name    #名字
    tieba['detail']['detail_content'] = detail_content    #内容
    tieba['detail']['detail_img'] = detail_img    #内容中图片链接
    tieba['detail']['detail_video'] = detail_video    #内容中视频链接

    print(tieba)


