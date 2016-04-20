#coding:UTF8
'''
@author: linsen
'''


import html_downloader, html_parser
import db_data, file_handle
from pip._vendor.requests.packages import chardet
import time


class NovelMain(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.data = db_data.DbData()
        self.filelogs = file_handle.FileHandle()
        
        self.start_id = None
        
        #设置采集多久后退出
        self.outtime = 3600
        
        #domain_id保存文件
        self.domainpath = 'domain.txt';
    
    
    def _domain_array(self, domain):
        self.domain_id = int(domain[0])
        self.domain = domain[1].encode('utf-8')
        self.name = domain[2]
        self.book_regular = domain[3].encode('utf-8')
        self.book_mark_id = domain[4].encode('utf-8')
        self.bookname_regular = domain[5].encode('utf-8')
        self.author_regular = domain[6].encode('utf-8')
        self.descript_regular = domain[7].encode('utf-8')
    
        
    def craw(self):
        start_time = time.time()
        
        domain = self.data.get_domain(self.domainpath)
        if domain is None:
            self.filelogs.writeLogs('domain is None')
            exit()
        
        self._domain_array(domain)
        
        if self.domain_id and self.domain_id is not None:
            self.filelogs.writeFile(self.domainpath, self.domain_id)
        
        self.filelogs.writeLogs('采集开始  ID:%d'%(self.domain_id))
        
        #统计连续失败的次数
        fail_count = 0
        
        #print domain
        while (time.time() - start_time) <= self.outtime:
            new_url = self.book_regular
            
            #补全链接中的http
            domian_host = self.parser.get_http_url(self.domain)
            
            self.start_id = self.data.get_book_id(self.domain_id, self.start_id)
            
            #组装book_id 的 url
            full_url = self.parser.fill_url_book_id(new_url, self.start_id, self.book_mark_id)
            
            if full_url and full_url != '':
                self.filelogs.writeLogs('下载页面开始')
                html_cont = self.downloader.download(full_url)
                self.filelogs.writeLogs('下载页面结束')
                
                if html_cont is None:
                    fail_count = fail_count + 1
                else:
            
                    if chardet.detect(html_cont)['encoding'] == 'GB2312' or chardet.detect(html_cont)['encoding'] == 'gb2312':
                        iconv_type = 'gbk'
                    else:
                        iconv_type = chardet.detect(html_cont)['encoding']
               
                    html_cont_coding =  html_cont.decode(iconv_type,'ignore').encode('utf-8')
                 
                 
                    #获取book_id
                    book_id = self.start_id
                    book_id = int(book_id)
                    #获取小说名称
                    book_name = self.parser.get_book_name(html_cont_coding, self.bookname_regular)
                     
                    #获取作者名称
                    author = self.parser.get_author(html_cont_coding, self.author_regular)
                     
                    #获取简介
                    descript = self.parser.get_descript(html_cont_coding, self.descript_regular)
                    #去除开通的空格
                    if descript is not None:
                        descript = self.parser.del_space(descript)
                     
                    if book_name is not None and author is not None:
                        fail_count = 0
                        #把小说信息存入数据库
                        self.data.save_book(self.domain_id, book_id, book_name, author, descript)
                    else:
                        fail_count = fail_count + 1
                
                #连续失败50次，停止采集
                if fail_count == 50:
                    self.filelogs.writeLogs('失败次数：'+str(fail_count))
                    break
                
            if (time.time() - start_time) > self.outtime:
                break
            
        self.filelogs.writeLogs('采集结束')
    
    



if __name__=="__main__":
    obj_spider = NovelMain()
    obj_spider.craw()