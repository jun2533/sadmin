#!/usr/bin/env python
#coding:utf-8
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    user_type = models.ForeignKey('UserGroup')

class UserGroup(models.Model):
    groupname = models.CharField(max_length=50)
    
    
    def __unicode__(self):
        return self.groupname
    
class Svname(models.Model):
    sname = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.sname
  
class Svnversion(models.Model):
    sname = models.ForeignKey('Svname')
    version = models.IntegerField()
    
class FileList(models.Model):
    filename = models.CharField(max_length=10)   

class FileRole(models.Model):    
    rolename = models.CharField(max_length=5)

class MysqlEnv(models.Model):
    envname = models.CharField(max_length=50)


class Mysqlname(models.Model):
    mname = models.CharField(max_length=50)
      
