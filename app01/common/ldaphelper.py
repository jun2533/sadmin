#!/usr/bin/env python
#coding:utf-8
import sys
sys.path.append("/usr/lib64/python2.6/site-packages")

import ldap

LDAP_HOST = '192.168.0.12'
LDAP_BASE_DN = 'dc=orange5s,dc=com'
MGR_CRED = 'cn=admin,dc=orange5s,dc=com'
MGR_PASSWD = 'orange5s'
STOOGE_FILTER = 'uid=*'

class LDAPMgmt:
    def __init__(self,ldap_host=None, ldap_base_dn=None, mgr_cred=None, mgr_passwd=None):
        if not ldap_host:
            ldap_host = LDAP_HOST
        if not ldap_base_dn:
            ldap_base_dn = LDAP_BASE_DN
        if not mgr_cred:
            mgr_cred = MGR_CRED
        if not mgr_passwd:
            mgr_passwd = MGR_PASSWD
        try:
            self.ldapconn = ldap.open(ldap_host)
            self.ldapconn.simple_bind(mgr_cred, mgr_passwd)
            self.ldap_base_dn = ldap_base_dn
        except ldap.LDAPError,e:
            print e
    
    def list_stooges(self,stooge_filter=None,attrib=None):
        if not stooge_filter:
            stooge_filter = STOOGE_FILTER
        s = self.ldapconn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, stooge_filter, attrib)
        
        stooge_list = []
        for stooge in s:
            attrib_dict = stooge[1]
            #print attrib_dict
            for a in attrib:
                out = "%s: %s" % (a,attrib_dict[a])
                print out
                stooge_list.append(out)
                
        return stooge_list
    
    def add_stooge(self,stooge_name,stooge_ou,stooge_info):
        stooge_dn = 'uid=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        stooge_attrib = [(k, v) for (k, v) in stooge_info.items()]
        print "Adding stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.add_s(stooge_dn, stooge_attrib)
    
    def delete_stooge(self,stooge_name,stooge_ou):
        stooge_dn = 'uid=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        print "Deleting stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.delete_s(stooge_dn)

if __name__ == "__main__":
    l=LDAPMgmt()
    stooge_name = 'yj'
    print type(stooge_name)
    stooge_ou = 'design'
    stooge_info = {'cn':['xcw'],'givenname':['你好'],'mail':['test@123.com'],
                   'objectclass':['top','person','inetOrgPerson','shadowAccount'],
                   'sn':['好'],'uid':[stooge_name],'userpassword':['ttttt'],}
    #print stooge_info
    #l.add_stooge(stooge_name,stooge_ou,stooge_info)
    #l.list_stooges(attrib=['uid','cn','mail','sn'])
    #l.delete_stooge(stooge_name,stooge_ou)
    
    
        