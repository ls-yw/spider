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
        self.domians = set()
        self.book_ids = set()
    
    

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
            
            row = self.mysql.query("INSERT INTO zks_books (`domain_id`,`book_id`,`name`,`description`,`author`,`create_time`) VALUES ('%d','%d','%s','%s','%s','%s')"%(domain_id, book_id, book_name, descript, author, time.strftime("%Y-%m-%d %X", time.localtime())))
            if row:
                self.book_ids.add(book_id)
                
            else:
                return None
        else:
            return None
            
    
    
    def _get_domain(self,domian_id):
        if domian_id is None or domian_id == '':
            sql = 'select * from zks_domain order by id asc limit 0,1'
        else:
            sql = 'select * from zks_domain where id > %d order by id asc limit 0,1'%(int(domian_id))
            
        lists = self.mysql.fetchall(sql)
        
        if len(lists) == 0:
            return self._get_domain(None);
        
        for list in lists:
            return list
    
    
    #获取需要采集的domain
    def get_domain(self,domainpath):
        domian_id = self.filelogs.read_file(domainpath)
        return self._get_domain(domian_id)
        

    def _has_domains(self):
        return len(self.domians) != 0

    #判断该bookid是否已采集

    
    def _has_book_ids(self):
        return len(self.book_ids) != 0
    
    
    def get_book_ids(self,domain_id):
        lists = self.mysql.fetchall('select * from zks_books where domain_id = %d'%(domain_id))
        for list in lists:
            self.book_ids.add(int(list[2]))
    
    def is_collect(self,book_id,domain_id):
        if self._has_book_ids():
            if book_id in self.book_ids:
                return True
            else:
                return False
        else:
            self.get_book_ids(domain_id)
            if book_id in self.book_ids:
                return True
            else:
                return False

    
    
    
    
    

