#coding:UTF8
'''
@author: linsen
'''
#import BeautifulSoup
# from bs4 import BeautifulSoup
#from urllib.parse import urlparse
import re
import urlparse


class HtmlParser(object):
    
    
    
    #补全地址
    def get_full_url(self,baseurl,url):
        full_url = urlparse.urljoin(baseurl, url)
        return full_url
    
    def get_http_url(self,url):
        if re.match(r'http://|https://', url) is None:
            return 'http://'+url
        else:
            return url
     
    #获取小说名称
    def get_book_name(self, html_cont, preg):
        preg = self._dealPreg(preg)
        result = re.search(r''+preg, html_cont)
         
        if result is not None:
            return result.group(1)
        else:
            return None
     
    #获取作者名称 
    def get_author(self, html_cont, preg):
        preg = self._dealPreg(preg)
         
        result = re.search(r''+preg, html_cont)
        #print result
        if result is not None:
            return result.group(1)
        else:
            return None
     
    #获取简介
    def get_descript(self, html_cont, preg):
        preg = self._dealPreg(preg)
        result = re.search(r''+preg, html_cont)
         
        if result is not None:
            return result.group(1)
        else:
            return None  
     
     
    #处理正则条件中的<{bookid}>
    def _dealPregBookId(self, preg):
        preg = re.sub(r'<{bookid}>', '(\d+)', preg)
        return self._dealPreg(preg)
     
    #处理正则规则
    def _dealPreg(self, preg):
        preg = re.sub(r'\$\$\$\$', '(\d+)', preg)
        preg = re.sub(r'\$', '\d+', preg)
         
        preg = re.sub(r'\*\*\*\*', '([\w\W]*)', preg)
         
        preg = re.sub(r'\?', '\?', preg)
        preg = re.sub(r'/', '\/', preg)
         
        preg = re.sub(r'!!!!', '([^<>]*)', preg)
        preg = re.sub(r'(\r\n)|(\n)', '[\r\n|\n]*', preg)
         
        preg = re.sub(r'@', '&nbsp;', preg)
        return preg

    #填充book_id进url
    def fill_url_book_id(self,url,book_id, book_mark_id):
        book_mark_id = self.preg_book_id(book_id, book_mark_id)
        
        mark_id = self._get_url_calc(book_mark_id)
        
        url = re.sub(r'<{markid}>', str(mark_id), url)
        
        url = self.preg_book_id(book_id, url)
        return url
    
    #计算标记运算
    def _get_url_calc(self,strnum):
        res = strnum.split('+')
        
        if len(res) == 2:
            return int(res[0]) + int(res[1])
        
        res = strnum.split('-')
        if len(res) == 2:
            return int(res[0]) - int(res[1])
        
        res = strnum.split('*')
        if len(res) == 2:
            return int(res[0]) * int(res[1])
        
        res = strnum.split('%%')
        if len(res) == 2:
            return int(res[0]) / int(res[1])
        
        res = strnum.split('%')
        if len(res) == 2:
            return int(res[0]) % int(res[1])
    
    #替换book_id标记
    def preg_book_id(self,book_id,content):
        content = re.sub(r'<{bookid}>', str(book_id), content)
        return content
    
    #去除空格
    def del_space(self,cont):
        cont = re.sub(r'^(&nbsp;)+', '', cont)
        return cont
    
    
    
    

    
    
    
    

    
    
    

    
    
    
    

    
    
    
    
    
    
    



