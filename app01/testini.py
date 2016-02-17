#!/usr/bin/env python
#coding:utf-8

import ConfigParser
'''
cf = ConfigParser.RawConfigParser()
cf.read("test.conf")
secs = cf.sections()  
print 'sections:', secs  
#print cf.get("sec_b","b_key4")
#cf.set("sec_b","b_key4","aaaaaaaa")
#print cf.get("sec_b","b_key4")

opts = cf.options("sec_a")
print 'options:', opts  

kvs = cf.items("sec_a")
print 'sec_a:', kvs

str_val = cf.get("sec_a", "a_key1")
int_val = cf.getint("sec_a", "a_key2")
print "value for sec_a's a_key1:", str_val
print "value for sec_a's a_key2:", int_val  

cf.set("sec_b", "b_key3", "new-$r")
cf.set("sec_b", "b_newkey", "new-value") 
cf.add_section('a_new_section')  
cf.set('a_new_section', 'new_key', 'new_value')
cf.write(open("test.conf", "w"))
'''
cf = ConfigParser.RawConfigParser()
cf.read("orange5s.authz")
secs = cf.sections()  
#print 'sections:', secs  
kvs = cf.items("groups")
#print 'sec_a:', kvs
str_val = cf.get("groups", "dev")
l=str_val.split(",")

#print l.append("bbbb")
l.remove("dby")
print l
