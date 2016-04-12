#coding:UTF8
'''
@author: linsen
'''


import url_manager, html_downloader, html_parser,\
    html_outputer
from novel import db_data


class NovelMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.data = db_data.DbData()
    
    
    def craw(self):
        count = 1
        domain = self.data.get_domain()
        self.urls.add_new_url(domain[1])
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
#                 print('craw %d : %s'%(count, new_url))
                html_cont = self.downloader.download('http://'+new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)  
#                 self.urls.add_new_urls(new_urls)
#                 self.outputer.collect_data(new_data)
#                 
#                 if count == 1000:
#                     break
#                 
#                 count = count + 1
            except:
                print('craw failed')
#     
#         self.outputer.output_html()
    

    
    



if __name__=="__main__":
    obj_spider = NovelMain()
    obj_spider.craw()