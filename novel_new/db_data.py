#coding:utf8
'''
Created on 2016年4月12日

@author: user
'''
import db_mysql,file_handle
import time


class DbData(object):
    def __init__(self):
        self.mysql = db_mysql.DbMysql()
        self.filelogs = file_handle.FileHandle()
    
    

    #判断该book_id是否已存入过数据库
    def _is_insert(self,domain_id,book_id):
        count = self.mysql.query("select id from zks_books where domain_id=%d and book_id=%d"%(domain_id,book_id))
        if count > 0:
            return True
        else:
            return False
    
    #把小说信息存入数据库
    def save_book(self, domain_id, book_id, book_name, author, descript):
        if self._is_insert(domain_id,book_id) is False:
            
            self.mysql.query("INSERT INTO zks_books (`domain_id`,`book_id`,`name`,`description`,`author`,`create_time`) VALUES ('%d','%d','%s','%s','%s','%s')"%(domain_id, book_id, book_name, descript, author, time.strftime("%Y-%m-%d %X", time.localtime())))
            
        else:
            return None
            
    
    
    def _get_domain(self,domian_id):
        if domian_id is None or domian_id == '':
            sql = 'select * from zks_domain where is_open = 1 order by id asc limit 0,1'
        else:
            sql = 'select * from zks_domain where is_open = 1 and id > %d order by id asc limit 0,1'%(int(domian_id))
            
        lists = self.mysql.fetchall(sql)
        
        if len(lists) == 0:
            return self._get_domain(None);
        
        for list in lists:
            return list
    
    
    #获取需要采集的domain
    def get_domain(self,domainpath):
        domian_id = self.filelogs.read_file(domainpath)
        return self._get_domain(domian_id)
        
    
    
    #获取book_id开始点
    def get_book_id(self,domain_id, start_id):
        if start_id is None:
            return self._get_sql_book_id(domain_id)
        else:
            return start_id + 1
    
    def _get_sql_book_id(self, domain_id):
        sql = "select * from zks_books where domain_id=%d order by book_id desc limit 0,1"%(domain_id)
        row = self.mysql.fetchall(sql)
        
        if len(row) == 0:
            return 1
        else:
            return int(row[0][2])+1
    

    
    
    
    
    

