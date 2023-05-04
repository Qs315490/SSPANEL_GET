import requests

class tempEmail:
    def __init__(self,email_id,passwd='00000000') -> None:
        self.email_id = email_id
        self.passwd = passwd
        self.email=''
        self.id=''
        self.session = requests.session()
        self.api_url = "https://api.mail.tm/"

    def get_domains(self):
        """获取域名"""
        back = self.session.get(self.api_url+'domains').json()
        return back['hydra:member'][0]['domain']
    
    def register(self):
        """注册邮箱"""
        back = self.session.post(self.api_url+'accounts',json={'address':self.email_id + '@' + self.get_domains(),'password':self.passwd}).json()
        try:
            print(back['hydra:description'])
        except:
            self.email = back['address']
            self.id = back['id']
        return back
    
    def login(self):
        """登录邮箱"""
        if self.email == '':
            self.email = self.email_id + '@' + self.get_domains()
        back = self.session.post(self.api_url+'token',json={'address':self.email,'password':self.passwd}).json()
        try:
            self.session.headers['Authorization'] = 'Bearer '+back['token']
            self.id = back['id']
        except:
            pass
        return back
    
    def del_email(self):
        """删除邮箱"""
        if self.id == '':
            return '未注册邮箱'
        back = self.session.delete(self.api_url+'accounts/'+self.id).json()
        return back
    
    def get_messages(self):
        """获取邮件列表"""
        back = self.session.get(self.api_url+'messages').json()
        return back
    
    def get_message(self,message_id):
        """获取邮件"""
        back = self.session.get(self.api_url+'messages/'+message_id).json()
        return back
    
if __name__ == "__main__":
    """测试"""
    temp_email = tempEmail('test987654')
    print(temp_email.get_domains())
    #print(temp_email.register())
    print(temp_email.login())
    print(temp_email.id)
    back=temp_email.get_messages()
    print(back)
    if back['hydra:totalItems'] != 0:
        id=back['hydra:member'][0]['id']
        print(temp_email.get_message(id)['html'][0])
    #print(temp_email.del_email())