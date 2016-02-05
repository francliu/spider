__author__ = 'liujianfei'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import random
import requests
import string

class CookieLogin:
    #页面初始化
    def __init__(self):
        self.fileName = 'cookie.txt'
        self.siteURL = 'https://passport.csdn.net/'
        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        self.cookie = cookielib.MozillaCookieJar(self.fileName)
        #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        self.handler= urllib2.HTTPCookieProcessor(self.cookie)
        
        self.postdata = urllib.urlencode({
                    'userName':'liujianfei526@163.com',
                    'pwd':''
                })
        self.loginHeaders =  {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
            'Referer': 'ttp://passport.csdn.net/account/login',
            'Connection' : 'keep-alive'
        } 
        self.pageNum = 0
        # use proxy ip 
        #self.ips_list = ['222.186.12.180:55336']
        #print '使用的代理ip地址： ' + self.ip
        #self.proxy_support = urllib2.ProxyHandler({'http':'http://'+random.choice(self.ips_list)})
        self.opener = urllib2.build_opener(self.handler)
        #通过handler来构建opener
        #self.opener = urllib2.build_opener(self.handler)
        urllib2.install_opener(self.opener)
    def getLoginInfo(self):
        #loginPage = self.opener.open(self.siteURL).text
        loginPage = self.opener.open(self.siteURL).read()
        pattern = re.compile('<input type="hidden".*?value="(.*?)" />',re.S)
        result = re.findall(pattern,loginPage)
        lt = result[0]
        execution = result[1]
        #print lt,execution
        self.postdata = urllib.urlencode({
                    "lt": lt,
                    "execution": execution,
                    "_eventId": "submit",
                    'username':'liujianfei526@163.com',
                    'password':''
                })
        #print self.postdata
    def login(self):
        #print self.postdata
        #模拟登录，并把cookie保存到变量
        request = urllib2.Request(self.siteURL,self.postdata,self.loginHeaders) 
        try:
            response = self.opener.open(request)
        except urllib.error.URLError as e:
            print(e.reason)
        #保存cookie到cookie.txt中
        #print result
        self.cookie.save(ignore_discard=True, ignore_expires=True) 
        print "ok"
#if __name__ == '__main__': 	
    #login = CookieLogin()
    #login.getLoginInfo()
    #login.login()
    #login.getPageNum("http://write.blog.csdn.net/postlist")
    #print result
