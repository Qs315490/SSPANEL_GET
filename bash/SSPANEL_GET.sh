#!/bin/bash
# 2022/6/18 21:02
# Power By Qs315490

# 默认配置文件名
configfile=config.yml

getconf()
{
	# 判断是否存在配置文件
	if [ -f $configfile ]
	then
		conf=$( cat $configfile | grep "$1" | awk '{print $2}' )
	fi
	echo ${conf:-$2}
}

# 此处为解析脚本接收的参数
if [ $1 ];then
	if [ -f $1 ];then
		configfile=$1
	else
		url=$1
	fi
fi

# 获取配置项
url=${url:-$( getconf url 5.52vpn.club )}
tok=${2:-`getconf tok b=3`}
domain=${2:-`getconf domain qq.com`}

# 验证码系统
vcode=$(getconf vcode)
if [[ "geetest" =~ "$vcode" ]]
then
	vcode="&geetest_challenge=d1fe173d08e959397adf34b1d77e88d7f7&geetest_validate=75775555755555e84_555557757550_755555775579b13&geetest_seccode=75775555755555e84_555557757550_755555775579b13|jordan"
fi

# 随机生成
email=$(tr -dc 0-9 < /dev/urandom | head -c10)

# 邮箱显示
echo $email@$domain

#curl环境
curl_path="curl -4 -s"

# 注册
back=`$curl_path "https://$url/auth/register" -X POST -d "email=$email%40$domain&name=zido&passwd=00000000&repasswd=00000000&wechat=$email&imtype=2$vcode" -c cookie`
echo -e $back
if ! echo -e $back|grep -q 1;then
	echo 注册失败
	exit
fi
# 登录
back=`$curl_path -b cookie "https://$url/auth/login" -X POST -d "email=$email%40$domain&passwd=00000000&code" -c cookie`
echo -e $back
if ! echo -e $back|grep -q 1;then
	echo 登录失败
	exit
fi
# 获取订阅码
$curl_path -b cookie "https://$url/user" | sed 's/"/\n/g' | grep "$tok" | head -n 1 > add.txt

# 输出
if [ `ls -l add.txt|awk '{print $5}'` != 0 ]
then
	echo "" # 空出一行
	cat add.txt
else
	echo 无法获取订阅码
	read -n 1
fi
