#!/usr/bin/env python
#coding:utf-8

import ConfigParser

import hashlib,os
from base64 import encodestring as encode

def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest()+salt)
    
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