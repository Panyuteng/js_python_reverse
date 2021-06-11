from Crypto.Cipher import AES
import base64
import requests
import json
import re
import time
from gevent import monkey
import gevent
monkey.patch_all()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

d = '{"rid":"R_SO_4_186421","threadId":"R_SO_4_186421","pageNo":12,"pageSize":"20","cursor":1617208352807,"orderType":"1","csrf_token":""}'
e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
encSecKey = '1206a2796de825fceaa6d57bbfaf901ce9c13c9f7364fb721aa1260355020a9e7e753744223f165be7a1b4edda2dbac2edda6add418de29793c177c1578611e606f9a35e3d8cb44da198072531528dc551416a6242d9330d410b066f410f6c9fab866cc6b2cc73131f62669042086f3666e3336bc5a2e0acb38ddef443a615da'
num = 0

def get_params():
    """
    获取params参数的值
    :return:
    """
    iv = "0102030405060708"
    i = '3XDOKTz8borjR3H3'
    # 获取密文
    encText = AES_encrypt(d, g, iv)
    encText = AES_encrypt(encText, i, iv)
    return encText


def AES_encrypt(text, key, iv):
    """
    进行aes加密
    :param text:加密的明文
    :param key:密钥
    :param iv:
    :return:
    """
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    encrypt_text = encryptor.encrypt(text.encode("utf-8"))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text.decode('utf8')


def get_html(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data, timeout=2)
    return response.text


def get_comments(mid):
    """
    抓取歌曲的评论
    :param mid: 歌曲id
    :return:
    """
    global d
    global num
    # 评论获取地址
    url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
    cursor = int(time.time() * 1000)

    for i in range(1, 100000):
        num += 1
        print(mid)
        print(num)
        try:
            if cursor:
                d = re.sub('"cursor":\d+', '"cursor":{}'.format(cursor), d)
            else:
                d = '{"rid":"R_SO_4_1851652156","threadId":"R_SO_4_1851652156","pageNo":1,"cursor":,"pageSize":"20","orderType":"1","csrf_token":""}'
            d = re.sub('"pageNo":\d+', '"pageNo":{}'.format(i), d)
            d = re.sub('"pageNo":\d+', '"pageNo":{}'.format(i), d)
            d = re.sub('"rid":".*?"', '"rid":"{}"'.format(mid), d)
            d = re.sub('"threadId":".*?"', '"threadId":"{}"'.format(mid), d)
            params = get_params()
            try:
                json_text = get_html(url, params, encSecKey)
            except:
                continue
            print(json_text)
            json_dict = json.loads(json_text)
            # 用于进行下次查询
            cursor = json_dict['data']['cursor']
            datas = json_dict['data']['comments']
            for item in datas:
                content = item['content']
                userid = item['user']['userId']
                name = item['user']['nickname']
                likedCount = item['likedCount']
                # print(content, userid, name, likedCount)
            if len(datas) < 20:
                break
        except Exception as e:
            print(e)
            break


def gevent_job(mid_lists):
    """
    协程任务
    :param mid_lists:
    :return:
    """
    for i in mid_lists:
        get_comments('R_SO_4_{}'.format(i))


if __name__ == "__main__":
    mids = {}
    for i in range(60000, 10000000):
        # 经分析，歌曲以数字为歌曲id，60000前多为不存在
        # 以数字的后两位为分割任务的依据
        if str(i)[-2] not in mids:
            mids[str(i)[-2]] = [i]
        else:
            mids[str(i)[-2]].append(i)
    jobs = []
    for key in mids:
        jobs.append(gevent.spawn(gevent_job, mids[key]))
    gevent.joinall(jobs)

