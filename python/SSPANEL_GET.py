import random
import requests as rq
import re

url = "1.swgj.xyz"
tok = "b=3"
vcode = "geetest"

# 生成邮箱
email_num = random.randint(100000000, 999999999)
print(str(email_num)+"@qs.com")

# 保持连接
web_session = rq.session()

def http(url="baidu.com", mode=0, pushdata={"", }):
    "0:GET 1:POST"
    if mode == 0:
        index = web_session.get(url, timeout=5)
    else:
        index = web_session.post(url, data=pushdata, timeout=5)
    return index

# 注册
def reg():
    "注册"
    # geetest验证的POST_data
    geetest = {"geetest_challenge": "98dce83da57b0395e163467c9dae521b1f",
            "geetest_validate": "bebe713_e80_222ebc4a0",
            "geetest_seccode": "bebe713_e80_222ebc4a0|jordan"}

    # POST_data
    data = {"email": str(email_num)+"@qs.com",
            "name": "zdzc",
            "passwd": "00000000",
            "repasswd": "00000000",
            "wechat": str(email_num),
            "imtype": "2"}

    # 添加验证方式
    if vcode == "geetest":
        data.update(geetest)

    back = http("https://"+url+"/auth/register", 1, data).json()["msg"]
    return back

# 登录
def login():
    "登录"
    data = {"email": str(email_num)+"@qs.com",
            "passwd": "00000000", "code": ""}
    back = http("https://"+url+"/auth/login", 1, data).json()["msg"]
    return back

# 登录用户中心
def user():
    "获取用户中心网页HTML"
    back = http("https://"+url+"/user", 0).text
    # 使用正则表达式获取订阅地址
    dy_url=re.search("https://[\w./?=&]+"+tok+"[\w=&]*",back).group(0)
    return dy_url

back = reg()
print(back)
if back == "注册成功！正在进入登录界面":
    back=login()
    print(back,end="\n\n")
    user_back=user()
    print(user_back)
