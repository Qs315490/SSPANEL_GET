import random
import re
import sys

import requests

url = "1.swgj.xyz"
tok = "b=3"
vcode = "geetest"
gui=False

def do_help():
    print(sys.argv[0], """[选项 [值]] 或 [选项=[值]]
    -u,--url URL    : 设置 URL
    -t,-token TOKEN : 设置 TOKEN
    --h,--help      : 显示这个帮助
    -g,--gui        : 开启图形界面 (没有实现)""")
    quit()

def do_rule(new_str: str, rule="."):
    "判断字符是否存在, 不存在退出程序"
    if rule in new_str:
        return new_str
    else:
        print("不符合规则: ", new_str)
        quit()

# 开始解析
i = 0
arg = sys.argv
while i < len(arg):
    if arg[i][0] == "-":
        if arg[i][1] == "-":
            if arg[i][2:5] == "url":
                if len(arg[i]) > 5 and arg[i][5] == "=":
                    # --url=(url)
                    url = do_rule(arg[i][6:])
                else:
                    # --url (url)
                    i += 1
                    url = do_rule(arg[i])
            elif arg[i][2:7] == "token":
                if len(arg[i]) > 7 and arg[i][7] == "=":
                    # --token=(token)
                    tok = do_rule(arg[i][8:], "=")
                else:
                    # --token (token)
                    i += 1
                    tok = do_rule(arg[i], "=")
            elif arg[i][2:] == "help":
                # --help
                do_help()
            elif arg[i][2:]=="gui":
                # --gui
                gui=True
        elif arg[i][1] == "u":
            if len(arg[i]) > 2 and arg[i][2] == "=":
                # -u=(url)
                url = do_rule(arg[i][3:])
            else:
                # -u=(url)
                i += 1
                url = do_rule(arg[i])
        elif arg[i][1] == "t":
            if len(arg[i]) > 2 and arg[i][2] == "=":
                # -t=(token)
                tok = do_rule(arg[i][3:], "=")
            else:
                # -t (token)
                i += 1
                tok = do_rule(arg[i], "=")
        elif arg[i][1] == "h":
            do_help()
        elif arg[i][1]== "g":
            # -g
            gui=True
    i += 1

# 生成邮箱
email_num = random.randint(100000000, 999999999)
print(str(email_num)+"@qs.com")

# 保持连接
web_session = requests.session()


def http(url="baidu.com", mode=0, pushdata={"", }):
    "0:GET 1:POST"
    if mode == 0:
        index = web_session.get(url, timeout=5)
    else:
        index = web_session.post(url, data=pushdata, timeout=5)
    return index

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
    dy_url = re.search("https://[\w./?=&]+"+tok+"[\w=&]*", back).group(0)
    return dy_url


back = reg()
print(back)
if back == "注册成功！正在进入登录界面":
    back = login()
    print(back, end="\n\n")
    user_back = user()
    print(user_back)
