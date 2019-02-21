import requests
from lxml import etree
import re

headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie":"TIEBA_USERTYPE=402bc30920a1467f2b74f4fc; BIDUPSID=4860AB12D180AA474CA3894B0A2C892E; BAIDUID=DF21A6DF36CEDD50476C260C7C5369F8:FG=1; PSTM=1545125782; BDUSS=TFUVUNUWnVFVDFIN21rcjRTQVpycVhWN2RQbHZtVE5NWWRvVEtwc3FWWkFLRUZjQVFBQUFBJCQAAAAAAAAAAAEAAADDs~lFnkXH6bXEtLrM7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAECbGVxAmxlcc; TIEBAUID=631700b06ca314238700130f; STOKEN=98b274d9039792ab4dfda38417298be2cd378f1c84a5dee32970e61ed5fca621; bdshare_firstime=1545183015459; 1173992387_FRSVideoUploadTip=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1545200732,1545200737,1545200788,1545267944; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1545291420; wise_device=0; BDRCVFR[9Do93j_AhCs]=ROUeEpQZVH_PH01nHD3QhPEUf; delPer=0; PSINO=3; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0",
}
reply = []
url = 'https://tieba.baidu.com/p/comment?tid=2612989431&pid=39381871997&pn=1'

resp = requests.get(url=url,headers=headers)

content = resp.content.decode('utf-8','ignore')

html = etree.HTML(content)

# divs = html.xpath('//div[@class="lzl_cnt"]')
# for div in divs:
#     reply_details = div.xpath('.//text()')
#     reply_detail = re.sub(r"[(回复)]","","".join(reply_details))
#     reply.append(reply_detail)

# nums = html.xpath('//p//a[last()]/@href')
#
# if len(nums) == 0:
#     break
# else:
#
# print(num)