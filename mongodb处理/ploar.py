import hashlib
import time
import random
import string
from urllib.parse import quote
import requests
import pymongo


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_params(plus_item):
    global params
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))

    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key  
    app_id = '2110900827'
    app_key = 'Z6gIDhi8NUSW6dcl'
    params = {'app_id': app_id,
              'text': plus_item,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              }
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def get_sentiments(comments):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"
    comments = comments.encode('utf-8')
    payload = get_params(comments)
    r = requests.post(url, data=payload)
    return r.json()

if __name__ == '__main__':
    client = pymongo.MongoClient("39.165.96.15", 27017)

    lis1 = client.weibo.WeiboItem.find(no_cursor_timeout = True) #默认10分钟，设为True永不关闭，手动关
    lis2 = client.tieba.tiebaitem.find(no_cursor_timeout = True)


    for i in lis1:
        print(i)
        try:
            ret = i["detail"]
            # len(ret)<=66才会正常响应，一个汉字占3个字节，上限200字节
            ret0 = ret[:66]
            data = get_sentiments(ret0)
            polar = data['data']['polar']
            client.datas.data.update_many({'_id': {'$eq': i['_id']}}, {'$set': {'data_emotion': polar}})
            client.weibo.WeiboItem.update_many({'_id': {'$eq': i['_id']}}, {'$set': {'emotion': polar}})
        except:
            continue
    lis1.close()    #关闭游标

    for m in lis2:
        print(m)
        try:
            ret1 = m["title"]
            # len(ret)<=66才会正常响应，一个汉字占3个字节，上限200字节
            ret2 = ret1[:66]
            data = get_sentiments(ret2)
            polar = data['data']['polar']
            client.datas.data.update_many({'_id': {'$eq': i['_id']}}, {'$set': {'data_emotion': polar}})
            client.tieba.tiebaitem.update_many({'_id': {'$eq': i['_id']}}, {'$set': {'emotion': polar}})
        except:
            continue

    lis2.close()



