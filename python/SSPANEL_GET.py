import random
import re
import sys
import threading
import tkinter
from tkinter import messagebox

try:
    import requests
except ImportError:
    print('[!] requests 模块未安装，请使用 pip3 install requests 安装')
    sys.exit(1)

url = "52vpn.club"
tok = "b=3"
vcode = "geetest"
gui = True if sys.platform == 'win32' else False
isDebug = True if sys.gettrace() else False


def do_help():
    print(sys.argv[0], """[选项 [值]] 或 [选项=[值]]
    -u,--url URL    : 设置 URL
    -t,-token TOKEN : 设置 TOKEN
    --h,--help      : 显示这个帮助
    -g,--gui        : 开启图形界面 (没有实现)""")
    quit()


def do_rule(new_str: str, rule="."):
    """判断字符是否存在, 不存在退出程序"""
    if rule in new_str:
        return new_str
    else:
        print("不符合规则: ", new_str)
        quit()


# 开始解析
i = 1
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
            elif arg[i][2:] == "gui":
                # --gui
                gui = True
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
        elif arg[i][1] == "g":
            # -g
            gui = True
    if "." in arg[i]:
        url = do_rule(arg[i])
    if "=" in arg[i]:
        tok = do_rule(arg[i], "=")
    i += 1

if isDebug:
    print("argv:", sys.argv)
    print("url:", url, end=" ")
    print("token:", tok)
    print("gui:", gui)


def get_email() -> int:
    # 生成邮箱
    return random.randint(100000000, 999999999)


# 保持连接
web_session = requests.session()


def http(http_url="baidu.com", http_pushdata=None):
    """0:GET 1:POST"""
    if http_pushdata is None:
        index = web_session.get(http_url, timeout=5)
    else:
        index = web_session.post(http_url, data=http_pushdata, timeout=5)
    return index


def reg():
    """注册"""
    # geetest验证的POST_data
    geetest = {"geetest_challenge": "98dce83da57b0395e163467c9dae521b1f",
               "geetest_validate": "bebe713_e80_222ebc4a0",
               "geetest_seccode": "bebe713_e80_222ebc4a0|jordan"}

    # POST_data
    data = {"email": str(email_num) + "@qs.com",
            "name": "zdzc",
            "passwd": "00000000",
            "repasswd": "00000000",
            "wechat": str(email_num),
            "imtype": "2"}

    # 添加验证方式
    if vcode == "geetest":
        data.update(geetest)

    reg_back = http("https://" + url + "/auth/register", data).json()["msg"]
    return reg_back


def login():
    """登录"""
    data = {"email": str(email_num) + "@qs.com",
            "passwd": "00000000", "code": ""}
    login_back = http("https://" + url + "/auth/login", data).json()["msg"]
    return login_back


# 登录用户中心


def user():
    """获取用户中心网页HTML"""
    http_back = http("https://" + url + "/user").text
    # 使用正则表达式获取订阅地址
    dy_url = re.search("https://[\\w./?=&]+{0}[\\w=&]*".format(tok), http_back).group(0)
    return dy_url


def __button():
    """获取订阅链接按钮被按下"""
    global url, tok, email_num
    url = entry_url.get()
    tok = entry_token.get()
    email_num = get_email()
    button.configure(state="disabled")
    entry_email.configure(state="normal")
    entry_email.select_clear()
    entry_email.insert(0, str(email_num) + "@qs.com")
    entry_email.configure(state="readonly")
    # 注册
    back_reg = reg()
    if back_reg == "注册成功！正在进入登录界面":
        button.configure(text=back_reg)
        # 登录
        back_login = login()
        if back_login == "登录成功":
            button.configure(text=back_login)
            # 获取用户中心网页HTML
            back_user = user()
            pyperclip.copy(back_user)
            entry_dy_url.configure(state="normal")
            entry_dy_url.select_clear()
            entry_dy_url.insert(0, back_user)
            entry_dy_url.configure(state="readonly")
        else:
            messagebox.showerror("错误", "登录失败！")
        button.configure(text="获取订阅链接")
    else:
        messagebox.showinfo("注册失败", back_reg)
    button.configure(state="normal")


if gui:
    try:
        import pyperclip
    except ImportError:
        print('[!] requests 模块未安装，请使用 pip3 install pyperclip 安装')
        sys.exit(1)

    root = tkinter.Tk()
    # 窗口标题
    root.title("订阅链接获取")
    # 窗口大小
    root.geometry("245x123")
    # 窗口图标
    # root.resizable(0, 0)
    # 窗口背景颜色
    root.configure(background="white")


    def button_click():
        """按钮点击事件"""
        threading.Thread(target=__button).start()


    # 窗口内容
    # 按钮
    button = tkinter.Button(root, text="获取订阅链接", width=267, font=("微软雅黑", 12), command=button_click)
    button.pack()

    # 标签_url
    label_url = tkinter.Label(root, text="订阅源", bg="white", font=("微软雅黑", 10))
    label_url.place(x=6, y=37)
    # 输入框_url
    entry_url = tkinter.Entry(root, width=20, font=("微软雅黑", 10))
    entry_url.insert(0, url)
    entry_url.place(x=60, y=37)

    # 标签_token
    label_token = tkinter.Label(root, text="token", bg="white", font=("微软雅黑", 10))
    label_token.place(x=7, y=57)
    # 输入框_token
    entry_token = tkinter.Entry(root, width=20, font=("微软雅黑", 10))
    entry_token.insert(0, tok)
    entry_token.place(x=60, y=57)

    # 标签_邮箱
    label_email = tkinter.Label(root, text="邮箱", width=6, bg="white", font=("微软雅黑", 10))
    label_email.place(x=0, y=77)
    # 文本框_邮箱
    entry_email = tkinter.Entry(root, width=20, state="readonly", font=("微软雅黑", 12))
    entry_email.place(x=60, y=77)

    # 标签_订阅链接
    label_dy_url = tkinter.Label(root, text="订阅地址", bg="white", font=("微软雅黑", 10))
    label_dy_url.place(x=0, y=97)
    # 文本框_订阅链接
    entry_dy_url = tkinter.Entry(root, width=20, state="readonly", font=("微软雅黑", 12))
    entry_dy_url.place(x=60, y=97)

    root.mainloop()
else:
    email_num = get_email()
    print(str(email_num) + "@qs.com")
    # 注册
    back = reg()
    print(back)
    if back == "注册成功！正在进入登录界面":
        # 登录
        back = login()
        print(back, end="\n\n")
        if back == "登录成功":
            # 获取用户中心网页HTML
            user_back = user()
            print(user_back)
