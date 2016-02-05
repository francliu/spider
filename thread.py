__author__ = 'liujianfei526@163.com'
# -*- coding:utf-8 -*-

import threading  
import time  
class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = 1  
        self.thread_stop = False  
    
    def run(self): #Overwrite run() method, put what you want the thread do here  
        while not self.thread_stop:  
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            time.sleep(self.interval)  
    def stop(self,flag):  
        self.thread_stop = flag  
            
    
def test():  
    thread1 = timer(1)  
    thread2 = timer(2)  
    thread1.start()  
    thread2.start()  
    time.sleep(10)  
    thread1.stop(True)  
    thread2.stop(True)  
    return  
    
if __name__ == '__main__':  
    test()  
