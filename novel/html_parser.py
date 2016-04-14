#coding:UTF8
'''
@author: linsen
'''
#import BeautifulSoup
from bs4 import BeautifulSoup
#from urllib.parse import urlparse
import re
import urlparse


class HtmlParser(object):
    
    
    
    #获取新的链接
    def _get_new_urls(self, page_url, soup, domain):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"^/|"+domain))
         
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            #new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
         
        return new_urls
     
     
    def _get_new_data(self, page_url, soup):
        res_data = {}
         
        res_data['url'] = page_url
         
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find("h1")  
        res_data['title'] = title_node.get_text()
         
        summary_node = soup.find('div', class_='lemma-summary') 
        res_data['summary'] = summary_node.get_text()
         
        return res_data
    
    def parse(self, page_url, html_cont, domain):
        if page_url is None or html_cont is None:
            return
        
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup, domain)
        return new_urls

    
    def get_http_url(self,url):
        if re.match(r'http://|https://', url) is None:
            return 'http://'+url
        else:
            return url

    
    
    
    def is_book_link(self, url, preg):
        preg = self._dealPregBookId(preg)
        return re.match(r'^'+preg, url) is not None
     
    #获取链接上的book_id        
    def get_book_id(self, url, preg):
        preg = self._dealPregBookId(preg)
        result = re.match(r'^'+preg, url)
         
        if result is not None:
            return result.group(1)
        else:
            return None
     
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

    
    
    
    

    
    
    

    
    
    
    

    
    
    
    
    
    
    



