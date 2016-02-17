#!/usr/bin/env python
#coding:utf-8
import sys
sys.path.append("/usr/lib64/python2.6/site-packages")

import ldap


LDAP_HOST='192.168.0.12'
USER = 'cn=admin,dc=orange5s,dc=com'
PASSWORD = 'orange5'
BASE_DN = 'dc=orange5s,dc=com'
    
class LDAPTool:
    
   
    
    def __init__(self,ldap_host=None,base_dn=None,user=None,password=None): 
        if not ldap_host:
            self.ldap_host = LDAP_HOST
        if not base_dn:
            self.base_dn = BASE_DN
        if not user:
            self.user = USER
        if not password:
            self.password = PASSWORD   
        
        
        try:
            self.ldapconn = ldap.open(ldap_host) 
            self.ldapconn.simple_bind(user,password)
        except ldap.LDAPError,e: 
            print e


    def ldap_get_user(self,uid=None):
        obj = self.ldapconn
        obj.protocal_version = ldap.VERSION3
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None
        searchFilter = "cn=" + uid 
        try:
            ldap_result_id = obj.search(self.base_dn, 
                                         searchScope, 
                                         searchFilter, 
                                         retrieveAttributes) 
            result_type, result_data = obj.result(ldap_result_id, 0) 
            if result_type == ldap.RES_SEARCH_ENTRY:
                username = result_data[0][1]['cn'][0]
                email = result_data[0][1]['mail'][0]
                nick = result_data[0][1]['sn'][0]
                result = {'username':username,'email':email,'nick':nick}
                return result
            else:
                return None
        
        except ldap.LDAPError,e: 
            print e
            
    def  ldap_user(self):
        print self.ldap_host
        
u = LDAPTool()
u.ldap_user()