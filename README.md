# JavBusCrawlerToAria2
自动爬取所有磁力搜索结果并提交到Aria2下载

例如

--name 某车牌号前缀（如GIRO)

他会自动搜索javbus上所有前缀结果（整个系列），全部提交到aria2下载


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

# 下载策略

多个文件挑选最大的

