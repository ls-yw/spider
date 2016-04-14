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
        try:
            response = urllib2.urlopen(request)   #2.7
#             response = urllib.urlopen(url)   #3
        except urllib2.URLError, e:
            self.filelogs.writeLogs(e.reason)
        
        if response.getcode() != 200:
            self.filelogs.writeLogs(url+' 状态：'+response.getcode())
            return None
        
        return response.read()
    
    



