#coding:UTF8
'''
@author: linsen
'''

import urllib
import urllib2


class HtmlDownloader(object):
    
    
    def download(self, url):
        if url is None:
            return None
        
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer' : url}
        request = urllib2.Request(url,None,headers)
        response = urllib2.urlopen(request)   #2.7
        #response = urllib.request.urlopen(url)   #3
       
        if response.getcode() != 200:
            print response.getcode()
            return None
        
        return response.read()
    
    



