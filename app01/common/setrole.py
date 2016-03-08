#!/usr/bin/env python
#coding:utf-8

import sys,subprocess,os
import MySQLdb,time

reload(sys)
sys.setdefaultencoding('utf-8')

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
    
    def fetchAllRows(self):
        '返回结果列表'
        return self._cur.fetchall()
    
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
    
    def commit(self):
        '数据库commit操作'
        self._conn.commit()
    
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
    #os.chdir(u'/appdata/Design/设计部数据库/')
    #print os.getcwd()
    r = []
    fl= []
    fpath='/appdata/Design/设计部数据库/'
    dbconfig = {'host':'192.168.0.20', 
                'port': 3306, 
                'user':'root', 
                'passwd':'a8804873', 
                'db':'sadmin', 
                'charset':'utf8'}
    db = MySQL(dbconfig)
    sql =["SELECT * FROM `app01_userinfo` where id=%s" %(sys.argv[2]),
          "SELECT * FROM `app01_userlist` where username_id=%s" %(sys.argv[2])]
    for s in sql:
        db.query(s)
        r.append(db.fetchAllRows())
    db.close()
    
    username=r[0][0]['username']
    if sys.argv[1] == '1':
        for f in (r[1][0]['rfile']).split(","):
            fl.append(fpath + f)
        rflag = 'rx'
    else:
        for f in (r[1][0]['wfile']).split(","):
            fl.append(fpath + f)
        rflag = 'rwx'
    print rflag
    lfile=" ".join(fl)
    cmd = ['setfacl -R -m d:u:%s:%s %s' %(username,rflag,lfile),'setfacl -R -m u:%s:%s %s'%(username,rflag,lfile)]
    for c in cmd:
        #print c
        subprocess.call(c,shell=True)
    '''
    print r[0][0]['username']
    print r[1][0]['rfile']
    print ","join(r[1][0]['rfile']))
    username=r[0][0]['username']
    lfile =(r[1][0]['rfile']).split(",")
    print lfile
    role(sys.argv[1],username,lfile)
    '''
    '''
#role username file
    if sys.argv[1] == '1':
        print "read"
    else:
        print "wirte"

    usernameid=sys.argv[2]
    print usernameid
    for fileid in sys.argv[3:]:
        print fileid

#数据库连接参数  
    dbconfig = {'host':'192.168.0.12', 
                'port': 3306, 
                'user':'xcw_store', 
                'passwd':'WAswSSN9WkqvtpJL', 
                'db':'sadmin', 
                'charset':'utf8'}
#连接数据库，创建这个类的实例
    db = MySQL(dbconfig)
  
#操作数据库
    sql = "SELECT * FROM `app01_userlist` where username_id=%s" %(usernameid)
    db.query(sql)
  
#获取结果列表
    result = db.fetchAllRows()
  
#相当于php里面的var_dump
    db.close()
    print result
    '''