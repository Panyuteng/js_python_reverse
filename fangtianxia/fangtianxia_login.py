import execjs
import requests


def get_en_pwd(pwd):
    """
    获取加密的密码
    :param pwd:原始密码
    :return:
    """
    with open('my.js', 'r', encoding='utf8') as f:
        file = f.read()
        en_pwd = execjs.compile(file).call('get_password', pwd)
    return en_pwd


def login():
    username = 'test'
    pwd = '123456'
    en_pwd = get_en_pwd(pwd)
    data = {
        'uid': username,
        'pwd': en_pwd,
        'Service': 'soufun-passport-web',
        'AutoLogin': 1
    }
    headers = {
        # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Host": "passport.fang.com",
        # "Origin": "https://passport.fang.com",
        "Referer": "https://passport.fang.com/?backurl=https%3A%2F%2Fgz.fang.com%2F",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    url = 'https://passport.fang.com/login.api'
    r = requests.post(url, data=data, headers=headers)
    print(r.text)


if __name__ == '__main__':
    login()

