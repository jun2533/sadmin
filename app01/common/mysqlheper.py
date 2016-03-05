#!/usr/bin/env python
#coding:utf-8


import MySQLdb,time


class MySQL:
    error_code = ''
    _instance = None
    _conn = None
    _cur = None
    
    _TIMEOUT = 30
    _timecount = 0
    
    def __init__(self,dbconfig,):
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                                         port=dbconfig['port'],
                                         user=dbconfig['user'],
                                         passwd=dbconfig['passwd'],
                                         db=dbconfig['db'],
                                         charset=dbconfig['charset'])
        except MySQLdb.Error,e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            
            if self._timeout < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                raise Exception(error_msg)
            
            
        self._cur = self._conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        self._instance = MySQLdb


    def query(self,sql):
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQL.Error,e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result
    
    def update(self,sql):
        '执行 UPDATE 及 DELETE 语句'
        try:
            self._cur.execute("SET NAMES utf8") 
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result
    
    def insert(self,sql):
        '执行 INSERT 语句。如主键为自增长int，则返回新生成的ID'
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            return False
        
        
        
    def fetchAllRows(self):
        '返回结果列表'
        return self._cur.fetchall()
    
    def fetchOneRow(self):
        '返回一行结果，然后游标指向下一行。到达最后一行以后，返回None'
        return self._cur.fetchone()
    
    def getRowCount(self):
        '获取结果行数'
        return self._cur.rowcount
    
    def commit(self):
        '数据库commit操作'
        self._conn.commit()
        
    def rollback(self):
        '数据库回滚操作'
        self._conn.rollback()
        
    def __del__(self): 
        '释放资源（系统GC自动调用）'
        try:
            self._cur.close() 
            self._conn.close() 
        except:
            pass
        
    def  close(self):
        '关闭数据库连接'
        self.__del__()
        
if __name__ == '__main__':

#数据库连接参数  
    dbconfig = {'host':'localhost', 
                'port': 3306, 
                'user':'root', 
                'passwd':'a8804873', 
                'db':'sadmin', 
                'charset':'utf8'}
  
#连接数据库，创建这个类的实例
    db = MySQL(dbconfig)
  
#操作数据库
    sql = "SELECT * FROM `app01_userlist` where username_id=2"
    db.query(sql);
  
#获取结果列表
    result = db.fetchAllRows();
  
#相当于php里面的var_dump
    print result
  
  
#对行进行循环
    #for row in result:
#使用下标进行取值
        #print row[0]
    
#对列进行循环
        #for colum in row:
            #print colum
 
#关闭数据库
    db.close()
    print result[0]
    for i in result:
        print i['wfile']
        print i['rfile']