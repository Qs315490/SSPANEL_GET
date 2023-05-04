import random
import re
import sys

try:
    import requests
except ImportError:
    print('[!] requests 模块未安装，请使用 pip3 install requests 安装')
    sys.exit(1)

class SSPANEL_GET:
    def __init__(self, url="5.52vpn.club", token="b=3", vcode="geetest"):
        self.url = url
        self.token = token
        self.vcode = vcode
        self.session = requests.session()
        self.email_num = self.get_email()
        self.domain = 'qq.com'
        self.email_code=''
        
    def get_email(self) -> int:
    # 生成邮箱
        return random.randint(100000000, 999999999)

    def http(self,path,http_pushdata=None):
        http_url= f'https://{self.url}/{path}'
        if http_pushdata is None:
            req = self.session.get
        else:
            req = self.session.post
        
        return req(http_url, data=http_pushdata, timeout=5)

    def send_email(self,email=''):
        if email=='':
            email = str(self.email_num) + f"@{self.domain}"
        push_data={
            "email": email,
        }
        back = self.http('send',push_data).json()
        return back

    def reg(self):
        """注册"""
        # geetest验证的POST_data
        geetest = {"geetest_challenge": "98dce83da57b0395e163467c9dae521b1f",
                "geetest_validate": "bebe713_e80_222ebc4a0",
                "geetest_seccode": "bebe713_e80_222ebc4a0|jordan"}

        # POST_data
        data = {"email": str(self.email_num) + f"@{self.domain}",
                "name": "zdzc",
                "passwd": "00000000",
                "repasswd": "00000000",
                "wechat": str(self.email_num),
                "imtype": "2"}

        # 添加验证方式
        if "geetest" in self.vcode:
            data.update(geetest)

        if "email" in self.vcode:
            # TODO: 邮箱验证码
            # 需要自己处理验证码
            data.update({"emailcode": self.email_code})

        reg_back = self.http("auth/register", data).json()["msg"]
        return reg_back
    
    def login(self):
        """登录"""
        data = {"email": str(self.email_num) + f"@{self.domain}",
                "passwd": "00000000", "code": ""}
        login_back = self.http("auth/login", data).json()["msg"]
        return login_back

    def user(self):
        """获取用户中心网页HTML"""
        http_back = self.http("user").text
        return http_back

    def get_sub(self,str):
        """获取订阅地址"""
        sub_url = re.findall(f"https://[\\w./?=&]+{self.token}[\\w=&]*", str)[0]
        return sub_url

    def get_sub_url(self):
        """一行获取订阅地址"""
        self.reg()
        self.login()
        return self.get_sub(self.user())

