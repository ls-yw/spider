#coding:utf8
'''
Created on 2016年4月12日

@author: user
'''
from novel import db_mysql


class DbData(object):
    def __init__(self):
        self.mysql = db_mysql.DbMysql()
        self.domians = set()
        self.book_ids = set()
    

    def get_domains(self):
        lists = self.mysql.fetchall('select * from zks_domain where id = 2 order by id asc')
        
        for list in lists:
            self.domians.add(list)
    
    def get_domain(self):
        if self._has_domains():
            return self.domians.pop()
        else:
            self.get_domains()
            return self.domians.pop()

    def _has_domains(self):
        return len(self.domians) != 0

    #判断该bookid是否已采集

    
    def _has_book_ids(self):
        return len(self.book_ids) != 0
    
    
    def get_book_ids(self,domain_id):
        lists = self.mysql.fetchall('select * from zks_books where domain_id = %d'%(domain_id),)
        print lists
        for list in lists:
            a = list[2]
            #print unicode(a,'gbk')
            self.book_ids.add(a)
        print self.book_ids
        exit()
    
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
    
    

