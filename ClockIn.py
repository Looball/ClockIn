import requests
import json
from hashlib import md5
from urllib import parse
import time
import urllib3
import sys
urllib3.disable_warnings()


# --------------------------------------------------------------------------
phone = sys.argv[1]  # 换成成你的手机号
pwd = sys.argv[2]  # 换成你的密码
name = sys.argv[3]  # 姓 名
ID_card = sys.argv[4]  # 身份证号
College = sys.argv[5]  # 学院
profession = sys.argv[6]  # 专业
Class = sys.argv[7]  # 班级
student_ID = sys.argv[8]  # 学号
address = sys.argv[9]
lat = sys.argv[10]
lng = sys.argv[11]
Positioning = {"address":address,"lat":float(lat),"lng":lng,"code":"1"}
District = sys.argv[12]  # 地区 如河南省-郑州市-金水区
deviceToken = sys.argv[13]  # 参见deviceToken获取
sckey = sys.argv[14]  # sever酱sckey
# ---------------------------------------------------------------------------
session = requests.Session()
date = time.strftime('%Y-%m-',time.localtime())
day = int(time.strftime('%d',time.localtime()))+1
date = date+str(day)

# Wxpush()消息推送模块
def Wxpush(msg):
    url = f'https://sc.ftqq.com/{sckey}.send?text={date}{msg}'
    requests.get(url)


# 指点天下登录模块
def login():
    url = 'http://app.zhidiantianxia.cn/api/Login/pwd'
    encoded_pwd = md5('axy_{}'.format(pwd).encode()).hexdigest()
    global flag
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '201',
        'Host': 'app.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.10.0'
    }
    data = {
        'phone': phone,
        'password': encoded_pwd,
        'mobileSystem': '9',
        'appVersion': '1.6.4',
        'mobileVersion': 'V1809A',
        'deviceToken': deviceToken,  # 换成你抓包得到的deviceToken
        'pushToken': '0868765546475757478765800CN01',
        'romInfo': 'hw'
    }

    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print('login_success!')
        flag = 1
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Wxpush(msg)
        flag = 0
    return response.json()['data']


# 每日健康打卡模块
def sign_in(token):
    url = 'http://zua.zhidiantianxia.cn/api/study/health/apply'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'V1809A(Android/9) (com.axy.zhidian/1.6.3) Weex/0.18.0 1080x2141',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '536'
    }
    datason = {"location": Positioning, "name": name, "phone": phone, "credentialType": "身份证",
               "credentialCode": ID_card,
               "college": College, "major": profession, "className": Class, "code": student_ID, "nowLocation": District,
               "temperature": "36.6", "observation": "否", "confirmed": "否", "goToHuiBei": "否", "contactIllPerson": "否",
               "isFamilyStatus": "否", "health": 0, "help": ""}
    data = {
        "health": 0,
        "student": "1",
        "content": str(datason)
    }
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        msg = '打卡成功'
        Wxpush(msg)
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Wxpush(msg)


# 获取每日宿舍签到的signInId模块
def get_signInId(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/my'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'user-agent': 'BKL-AL20(Android/10) (com.axy.zhidian/1.5.8) Weex/0.18.0 1080x2160',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    data = {
        'page': '0',
        'size': '10'
    }
    try:
        signInId = session.get(url=url, headers=header, data=data).json()['data']['content'][0]['id']
        return signInId
    except:
        pass


# 22点宿舍签到模块
def sign_in_evening(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/sign'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'BKL-AL20(Android/10) (com.axy.zhidian/1.5.8) Weex/0.18.0 1080x2160',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '146'
    }
    data = {
        "locale": str(Positioning["address"]),
        "lat": Positioning["lat"],
        "lng": Positioning["lng"],
        "signInId": get_signInId(token)
    }
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print("success!")
    else:
        print("fail!")
    msg = parse.quote_plus(response.json()['msg'])
    Wxpush(msg)

if __name__ =="__main__":
    token = login()

    time.sleep(3)
    now_H = int(time.strftime("%H"))
    if flag:
        if 14 <= now_H <= 15:      # 世界协调时间
            sign_in_evening(token)
        else:
            sign_in(token)
    else:
        pass
