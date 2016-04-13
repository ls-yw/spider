#coding:UTF8
'''
Created on 2016年4月12日
@author: user
'''
import MySQLdb
DatabaseError = MySQLdb.DatabaseError

class DbMysql(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.name = 'novel'
        self.user = 'root'
        self.pwd  = 'root'
        self.port = 3306
        self.charset='utf8'
        self._connection = None
    
    #连接数据库
    def _connect(self):
        try:
            self._connection = MySQLdb.connect(
                                host=self.host,
                                port=self.port,
                                user=self.user,
                                passwd=self.pwd,
                                db=self.name,     
                                charset=self.charset,
                                use_unicode=True   
                                )
        except MySQLdb.DatabaseError, e:
            raise DatabaseError('can not connect to MySQL://%s:%s, exception: %s' % (self.host, self.port, e.args[1]))
    
    #检测是不是有效连接
    def _vaid_connection(self):
        if self._connection is not None:
            try:
                self._connection.ping()
                return True
            except MySQLdb.DatabaseError:
                self._connection.close()
                self._connection = None
        return False
    
    #数据库游标
    def _cursor(self):
        if not self._vaid_connection():
            self._connect()
            self._connection.autocommit(1)
            #cursor = self._connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor = self._connection.cursor()
        else:
            #cursor = self._connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor = self._connection.cursor()
        return cursor
    
    # 关闭引用的数据库
    def close(self):
        if self._valid_connection():
            if self._trans is not None:
                self._connection.commit()
            self._connection.close()
            self._connection = None
    
    #执行sql操作
    def query(self,query,args=None):
        cursor = self._cursor()
        cursor.execute(query,args)
        self.affected_rows = self._connection.affected_rows()
        self.insert_id = self._connection.insert_id()
        cursor.close()
        return self.affected_rows
    
    # 获取全部结果
    def fetchall(self, query, args=None):
        cursor = self._cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    # 获取一个结果
    def fetchone(self, query, args=None):
        cursor = self._cursor()
        cursor.execute(query, args)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    
    
    
    
    