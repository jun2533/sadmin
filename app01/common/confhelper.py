#!/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ConfigParser
import hashlib,os
from base64 import encodestring as encode

def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest()+salt)

def setrole(role,ulist,mlist):
    r_list=[]
    w_list=[]
    for i in ulist:
        r_list=i.rfile.split(",")
        w_list=i.wfile.split(",")
  
    
   
    if role == '1':
        for i in mlist:
            if i not in r_list:
                r_list.append(i) 
            if i in w_list:
                w_list.remove(i)
    else:
        for i in mlist:
            if i not in w_list:
                w_list.append(i)
            if i in r_list:
                r_list.remove(i)
            
    
    while '' in r_list:
        r_list.remove('')
    
    while '' in w_list:
        w_list.remove('')
             
    srfile =",".join(r_list)
    swfile =",".join(w_list)    
    ulist.update(rfile=srfile)  
    ulist.update(wfile=swfile)

'''
class setrole():
    def __init__(self,role,ulist,mlist):
        self.role=role
        self.ulist=ulist
        self.mlist=mlist
        self.r_list=[]
        self.w_list=[]
        for i in self.ulist:
            self.r_list=i.rfile.split(",")
            self.w_list=i.wfile.split(",")
    
    def set(self):
        if self.role == '1':
            for i in self.mlist:
                if i not in self.r_list:
                    self.r_list.append(i) 
                if i in self.w_list:
                    self.w_list.remove(i)
        else:
            for i in self.mlist:
                if i not in self.w_list:
                    self.w_list.append(i)
                if i in self.r_list:
                    self.r_list.remove(i)
        
        while '' in self.r_list:
            self.r_list.remove('')
    
        while '' in self.r_list:
            self.w_list.remove('')
    
    def __del__(self):
        self.srfile =",".join(self.r_list)
        self.swfile =",".join(self.w_list)    
        self.ulist.update(rfile=self.srfile)  
        self.ulist.update(wfile=self.swfile)
'''

class conf():
    def __init__(self,cfile,ini,ou):
        
        self.cfile = cfile
        self.ini = ini
        self.ou = ou
        self.cf = ConfigParser.RawConfigParser()
        self.cf.read(self.cfile)
        #str_val = self.cf.get("groups", ou)
        str_val = self.cf.get(self.ini,self.ou)
        self.l=str_val.split(",")
    
    
    def add_user(self,user):
        self.l.append(user)
        print self.l
        #self.cf.set("groups", ou,",".join(l))
        #self.cf.write(open(self.cfile, "w"))
        
    def delete_user(self,user):
        self.l.remove(user)
        
    def __del__(self):
        self.cf.set(self.ini,self.ou,",".join(self.l))
        self.cf.write(open(self.cfile, "w"))
        #print "OK"
        


if __name__ == "__main__":
    c = conf("/appdata/Dev/orange5s.authz","groups","dev")
    #c.delete_user("ykkk1")
    
    print makeSecret("123@com")
    
    