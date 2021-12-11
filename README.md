# JavBusCrawlerToAria2
自动爬取所有磁力结果并提交到Aria2下载


# 环境要求

建议系统：Debian 10/11 || Ubuntu 18.04/20.04/21.04 || CentOS8

Python 3.4+

Selenium

ChromiumDriver

# 安装方法
apt install chromium-driver python3 python3-pip

python3 -m pip install selenium

# 使用方法

python3 JavBusCrawler.py --name xxx --host xx.xx.xx.xx --port xxxx --token xxxxxx


## 参数解释

name，javbus要搜寻的内容

host，Aria2地址

port，Aria2端口

token，Aria2密码（无密码不需要填）

