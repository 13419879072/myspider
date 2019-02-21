import requests
from lxml import etree


headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'showAdnanjing=1; global_cookie=5gd8anqu0yvsgcmmc79hu4zrp19jqf1lw67; integratecover=1; zixun_fang_layed=1; city=jy; Captcha=49515A667A4D6F72784F507767794231496157336A666A6F67645A4C6D366767617A6E64554F4D44344B76585776363869436B706359496A756C3439337A344B663131776E4672704636343D; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_xag9acd6b1mffnqinydw933gn29jqfx061s*3; ASP.NET_SessionId=vylo1eexjihzn2owuxjsdx3f; __utma=147393320.2098877557.1546425154.1546426999.1546477888.3; __utmb=147393320.9.10.1546477888; __utmc=147393320; __utmz=147393320.1546426999.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'referer': 'https://jy.zu.fang.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        }

url = 'https://jy.zu.fang.com/chuzu/3_319216040_1.htm?channel=1,2'

resp = requests.get(url=url,headers=headers)
content = resp.content.decode('gb2312','ignore')
html = etree.HTML(content)
ret = "".join(html.xpath('//p[@class="text_phone"]/text()|//div[@class="tjcont-jjr-line2 clearfix"]/text()')).replace(' ','').replace('\n','')

print(ret)