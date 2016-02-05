__author__ = 'liujianfei'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import removeUnsedTagTool
import os
import CookieLogin
import threading 
import time
import thread
mylock = thread.allocate_lock()
#抓取MM
class SpiderCSDN(threading.Thread):
    #页面初始化
    def __init__(self,part):
        threading.Thread.__init__(self)
        self.fileName = ''
        self.siteURL = ''
        self.tool = ''
        self.login = ''
        self.opener = ''
        self.postdata = ''
        self.loginHeaders = ''
        self.used = []
        self.unused = []
        self.hash = {}
        self.part = part
        self.thread_stop = False
    def setLoginInfo(self,fileName,siteURL,login,opener,tool,postdata,loginHeaders):
        '''设置用户登录信息'''
        self.fileName = fileName
        self.siteURL = siteURL
        self.login = login
        self.opener = opener
        self.tool = tool
        self.postdata = postdata
        self.loginHeaders = loginHeaders
    def run(self): #Overwrite run() method, put what you want the thread do here   
        self.getPageAllContent()
        print "结束时间"+time.ctime()
    def stop(self,flag):  
        self.thread_stop = flag 
    #处理异常
    def openAndDoExcept(self,url):
        request = urllib2.Request(url,self.postdata,self.loginHeaders)
        try:
            page = self.opener.open(request).read()
            self.saveList(self.unused,"unused")
        except urllib2.URLError, e:
            self.saveList(self.unused,"unused")
            self.saveList(self.used,"used")
            self.saveList(self.hash,"hash")
            if hasattr(e,"reason"):
                print u"连接糗事百科失败,错误原因",e.reason
                return None
        return page
    #获得相应页码文章
    def getPageNum(self,url):
        #利用cookie请求访问另一个网址
        page = self.openAndDoExcept(url)
        pattern = re.compile('<div class="page_nav"><span>.*?([\d]+).*?([\d]+).*?</span>',re.S)
        result = re.findall(pattern,page)
        #print page
        if result:
            #print "找到了共多少页"
            self.pageNum = result[0][1]
            #print '共',self.pageNum,'页'
            return self.pageNum
    #获得指定页码所有文章列表
    def getPageList(self,index):
        url = 'http://write.blog.csdn.net/postlist/0/0/enabled/'+str(index)
        page = self.openAndDoExcept(url)
        #<a href='' target=_blank></a>
        #<td class='tdleft'><a href='' target=_blank></a><span class='gray'>
        #获取相应的文章列表
        pattern = re.compile("<td class='tdleft'><a href='(.*?)'.*?target=_blank>(.*?)</a><span class='gray'>",re.S)
        result = re.findall(pattern,page)
        #print page
        if self.part!=1:
            if index%(self.part)==0:
                for i in result:
                    self.unused.append(i)
                    self.pageNum = i[0]
        else:
            if index%(2)!=0 and index%(3)!=0:
                for i in result:
                    self.unused.append(i)
                    self.pageNum = i[0]       
            #print i[0],i[1]
            #return self.pageNum
    #获得所有页码所有文章列表
    def getAllPageList(self,PageNum):
        #利用cookie请求访问
        for i in range(1,PageNum):
            #print "第"+str(i)+"页"
            self.getPageList(i)
        return self.unused
    #获得单篇文章内容并写入文档并保存
    def getPageContent(self,url):
        #利用cookie请求访问
        page = self.openAndDoExcept(url)
        listALl = url.split('/')
        name = listALl.pop()
        pattern = re.compile("<p>(.*?)</p>",re.S)
        if page!="":
            result = re.findall(pattern,page)
            #print result
            contentList = []
            for i in result:
                i = self.tool.replace(i)
                #print i
                #contentList.append(i)
                self.saveContent(i,name)
    #获得列表中所有文章内容并写入文档并保存
    def getPageAllContent(self):
        #利用cookie请求访问
        for num,i in enumerate(self.unused):
            #print num
            #mylock.acquire()
            #print "thread2"+str(num)+str(self.part)
            self.used.append(i);
            if self.hash.get(i[0])!=None:
                continue
            self.hash[i[0]]=i[1]
            self.getPageContent(i[0])
            #mylock.release()
        #self.stop(True)      
    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            #print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            #print u"名为",path,'的文件夹已经创建成功'
            return False
     #保存文章内容
    def saveList(self,content,name):
        fileName = "result" + '/' + name + ".txt"
        f = open(fileName,"w+")
        #print u"正在偷偷保存她的个人信息为",fileName
        for i in content:
            if len(i)>1:
                f.write(i[0]+'\n')
                #print i[0]
        f.close()
     #保存文章内容
    def saveContent(self,content,name):
        fileName = "result" + '/' + name + ".txt"
        f = open(fileName,"a+")
        #print u"正在偷偷保存她的个人信息为",fileName
        f.write(content+'\n')
        f.close()
if __name__ == '__main__': 	
    start_time = time.ctime()
    print "开始时间"+start_time
    fileName = "result"
    siteURL = "http://write.blog.csdn.net/postlist"
    login = CookieLogin.CookieLogin()
    login.getLoginInfo()
    login.login()
    opener = login.opener
    tool = removeUnsedTagTool.removeUnsedTagTool()
    csdn = SpiderCSDN(1);
    #初始化基本信息
    csdn.setLoginInfo(fileName,siteURL,login,opener,tool,login.postdata,login.loginHeaders)
    #print 'ok'
    #获取总页数
    PageNum = int(csdn.getPageNum(siteURL))+1
    #print PageNum
    csdn.getAllPageList(PageNum)
    csdn.mkdir("result")
    thread2 = SpiderCSDN(2)
    thread2.setLoginInfo(fileName,siteURL,login,opener,tool,login.postdata,login.loginHeaders)
    #获取总页数
    PageNum = int(thread2.getPageNum(siteURL))+1
    #print PageNum
    thread2.getAllPageList(PageNum)
    thread3 = SpiderCSDN(3)
    thread3.setLoginInfo(fileName,siteURL,login,opener,tool,login.postdata,login.loginHeaders)
    #获取总页数
    PageNum = int(thread3.getPageNum(siteURL))+1
    #print PageNum
    thread3.getAllPageList(PageNum)
    csdn.start()
    thread2.start()  
    thread3.start() 
    #Csdn.getPageAllContent()
    #Csdn.getPageContent('http://blog.csdn.net/liujianfei526/article/details/50597031')
    #print result