import requests
import json
from hashlib import md5
from urllib import parse
import time
import urllib3

urllib3.disable_warnings()

session = requests.Session()

# --------------------------------------------------------------------------
phone = '17516467303'  # 换成成你的手机号
pwd = '13166209219yml'  # 换成你的密码
name = "杨梦龙"  # 姓 名
shenfenzheng = '411729200011071213'  # 身份证号
xueyuan = '智能工程学院'  # 学院
zhuanye = '软件工程'  # 专业
banji = '19101101'  # 班级
xuehao = '1905170512'  # 学号
weizhi = {"address": "上海市上海市静安区天潼路619号",  # 换成自己的打卡定位地址
          "lat": 31.249161,  # 换成自己的签到定位维度信息
          "lng": 121.487899,  # 经度
          "code": "1"}
diqu = '上海市-市辖区-闵行区'  # 地区 如河南省-郑州市-金水区
deviceToken = '13065ffa4e6b403bf33'  # 参见deviceToken获取
uid = 'UID_pq4JDURb68ayfgnehqQKWZ0KHgVl'  # 接收消息的微信uid
# ---------------------------------------------------------------------------
evening_switch = 0  # 晚上宿舍签到开关，1为开启，0为关闭。不需要签到功能请把 "1" 改为 "0"
flag = False
nowtime = time.strftime("%Y-%m-%d", time.localtime())
Hour_Minutes = time.strftime('%H:%M')


# Qmsg消息推送模块
def Qmsg(msg, uid):
    url = f'http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_BxtNRNubGOsZLnd3u6RsQNgZxl9OF19X&content={nowtime}{msg}&uid={uid}'
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
        # 每个设备是唯一的不能随意更改
        'deviceToken': deviceToken,  # 换成你抓包得到的deviceToken
        'pushToken': '0868765037939765300003465800CN01',  # 可以随意更改
        'romInfo': 'hw'  # 可以随意更改
    }

    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print('login_success!')
        flag = True
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Qmsg(msg, uid)
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
    datason = {"location": weizhi, "name": name, "phone": phone, "credentialType": "身份证",
               "credentialCode": shenfenzheng,
               "college": xueyuan, "major": zhuanye, "className": banji, "code": xuehao, "nowLocation": diqu,
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
        Qmsg(msg, uid)
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Qmsg(msg, uid)


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
    # result = session.get(url=url,headers=header,data=data)
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
        "locale": "河南省郑州市金水区风华东路15号靠近郑州航空工业管理学院学生公寓18栋",  # 换成自己的签到定位地址
        "lat": "34.786959",  # 换成自己的签到定位维度信息
        "lng": "113.791111",  # 换成自己的签到定位经度信息
        "signInId": get_signInId(token)
    }
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    # title = '指点天下晚上签到结果'
    if response.json()['status'] == 1:
        print("success!")

    else:
        print("fail!")
    msg = parse.quote_plus(response.json()['msg'])
    Qmsg(msg, uid)


token = login()
time.sleep(3)
get_signInId(token)
time.sleep(3)
now_time = int(time.strftime("%H"))
if flag:
    if 22 <= now_time <= 23 and evening_switch == 1:
        sign_in_evening(token)
    else:
        sign_in(token)
else:
    pass
