#coding:UTF8
'''
@author: linsen
'''

import urllib


class HtmlDownloader(object):
    
    
    def download(self, url):
        if url is None:
            return None
        
        #response = urllib.urlopen(url)   #2.7
        response = urllib.request.urlopen(url)   #3
        
        if response.getcode() != 200:
            return None
        
        return response.read()
    
    



