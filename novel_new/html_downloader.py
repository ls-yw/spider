#coding:UTF8
'''
@author: linsen
'''

import urllib2,file_handle


class HtmlDownloader(object):
    def __init__(self):
        self.filelogs = file_handle.FileHandle()
    
    def download(self, url):
        if url is None:
            return None
        
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : url}
        request = urllib2.Request(url,None,headers)
        self.filelogs.writeLogs(str(url))
        try:
            response = urllib2.urlopen(request,timeout=30)   #2.7
#             response = urllib.urlopen(url)   #3
        except urllib2.URLError, e:
            print e
            if any(e):
                self.filelogs.writeLogs(e.reason)
            else:
                self.filelogs.writeLogs(e)
                if e == 'HTTP Error 504: Gateway Time-out':
                    exit()
            return None
        
        if response:
            if response.getcode() != 200:
                self.filelogs.writeLogs(url+' 状态：'+response.getcode())
                return None
            try:
                readcont = response.read()
                return readcont
            except:
                self.filelogs.writeLogs('read失败')
                return None
        else:
            return None
    
    



