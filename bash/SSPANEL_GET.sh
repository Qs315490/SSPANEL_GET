#!/bin/bash
# 2022/1/30 15:15
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
	if [ $conf ]
	then
		echo "$conf"
	else
		# 写出配置项
		# echo "$1: $2">>$configfile
		echo $2
	fi
}

# URL
url=$( getconf url cxkv2.xyz )
tok=$( getconf tok ?mu=2 )

# 此处为解析项
if [ $1 ];then
	if [ -f $1 ];then
		configfile=$1
	else
		url=$1
	fi
fi
if [ $2 ];then
	tok=$2
fi

# 验证码系统
vcode=$(getconf vcode)
if [ "geetest" = $vcode ]
then
	vcode="&geetest_challenge=d1fe173d08e959397adf34b1d77e88d7f7&geetest_validate=75775555755555e84_555557757550_755555775579b13&geetest_seccode=75775555755555e84_555557757550_755555775579b13|jordan"
fi

# 随机生成
email=$(tr -dc 0-9 < /dev/urandom | head -c10)

# 邮箱显示
echo $email@qs.com

#curl环境
curl_path="curl -4 -s"

# 注册
echo -e `$curl_path "https://$url/auth/register" -X POST -d "email=$email%40qs.com&name=zido&passwd=00000000&repasswd=00000000&wechat=$email&imtype=2$vcode" -c cookit`
# 登录
echo -e `$curl_path -b cookit "https://$url/auth/login" -X POST -d "email=$email%40qs.com&passwd=00000000&code" -c cookit`
# 获取订阅码
$curl_path -b cookit "https://$url/user" | sed 's/"/\n/g' | grep "$tok" | head -n 1 > add.txt

# 输出
if [ `ls -l add.txt|awk '{print $5}'` != 0 ]
then
	echo "" # 空出一行
	cat add.txt
else
	echo 无法获取订阅码
	read -n 1
fi
