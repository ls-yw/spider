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
    

    def get_domains(self):
        lists = self.mysql.fetchall('select * from zks_domain order by id')
        
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

