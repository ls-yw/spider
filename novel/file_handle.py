#coding:utf8
'''
Created on 2016年4月13日

@author: user
'''
import time
import os


class FileHandle(object):


    def writeLogs(self,preg):
        file_name = time.strftime("%Y-%m-%d", time.localtime())
        with open('logs/%s.txt'%(file_name), 'a') as f:
            f.write(time.strftime("%Y-%m-%d %X", time.localtime())+"\t")
            f.write(preg+"\n")

    def writeFile(self,filepath,content):
        with open(filepath, 'w') as f:
            f.write(str(content))

    #读取文件内容
    def read_file(self,filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
        else:
            return None
    
