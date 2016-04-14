#coding:UTF8
'''
@author: linsen
'''


import url_manager, html_downloader, html_parser,\
    html_outputer
from novel import db_data, preg, file_handle
from pip._vendor.requests.packages import chardet
import urlparse
import time


class NovelMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.data = db_data.DbData()
        self.preg = preg.Preg()
        self.filelogs = file_handle.FileHandle()
        
        #设置采集多久后退出
        self.outtime = 60*60
        
        #domain_id保存文件
        self.domainpath = 'domain.txt';
    
    
    def _domain_array(self, domain):
        self.domain_id = int(domain[0])
        self.domain = domain[1].encode('utf-8')
        self.name = domain[2]
        self.book_regular = domain[3].encode('utf-8')
        self.bookname_regular = domain[4].encode('utf-8')
        self.author_regular = domain[5].encode('utf-8')
        self.descript_regular = domain[6].encode('utf-8')
    
        
    def craw(self):
        start_time = time.time()
        
        domain = self.data.get_domain(self.domainpath)
        if domain is None:
            self.filelogs.writeLogs('domain is None')
            exit()
        print domain
        self._domain_array(domain)
        
        if self.domain_id and self.domain_id is not None:
            self.filelogs.writeFile(self.domainpath, self.domain_id)
        print self.domain_id
        exit()
        self.urls.add_new_url(self.domain)
        self.filelogs.writeLogs('采集开始  ID:%d'%(self.domain_id))
        #print domain
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                #补全链接中的http
                new_full_url = self.parser.get_http_url(new_url)
                #new_full_url = 'http://www.lingdiankanshu.com/html/1/1966/'
                #new_full_url = 'http://www.wn001.com/book/2284/'
                #new_full_url = 'http://www.zhukeshu.com'
                
                html_cont = self.downloader.download(new_full_url)
                #html_cont = self.downloader.download('http://www.wn001.com')
                if chardet.detect(html_cont)['encoding'] == 'GB2312' or chardet.detect(html_cont)['encoding'] == 'gb2312':
                    iconv_type = 'gbk'
                else:
                    iconv_type = chardet.detect(html_cont)['encoding']
                #print chardet.detect(html_cont)
                #str = unicode(html_cont,'gbk')
                html_cont_coding =  html_cont.decode(iconv_type).encode('utf-8')
                
                #判断url是否是小说目录url，True则采集该小说保存入数据库
                book_preg = urlparse.urljoin(new_full_url, self.book_regular)
                
                #是否是小说目录url
                if self.parser.is_book_link(new_full_url, book_preg):
                    #获取book_id
                    book_id = self.parser.get_book_id(new_full_url, book_preg)
                    book_id = int(book_id)
                    #判断该book_id是否已采集过
                    if self.data.is_collect(book_id, self.domain_id) is False:  #该book_id没采集过
                        #获取小说名称
                        book_name = self.parser.get_book_name(html_cont_coding, self.bookname_regular)
                        
                        #获取作者名称
                        author = self.parser.get_author(html_cont_coding, self.author_regular)
                        
                        #获取简介
                        descript = self.parser.get_descript(html_cont_coding, self.descript_regular)
                        
                        if book_name is not None and author is not None and descript is not None:
                            #把小说信息存入数据库
                            self.data.save_book(self.domain_id, book_id, book_name, author, descript)
                    
                    
                
                new_urls = self.parser.parse(new_url, html_cont_coding, self.parser.get_http_url(self.domain))  
                self.urls.add_new_urls(new_urls)
#                 self.outputer.collect_data(new_data)
                #exit()
                if (time.time() - start_time) > self.outtime:
                    self.filelogs.writeLogs('采集结束')
                    break
            except:
                self.filelogs.writeLogs('Faild:'+new_full_url)
#     
#         self.outputer.output_html()
    

    
    



if __name__=="__main__":
    obj_spider = NovelMain()
    obj_spider.craw()