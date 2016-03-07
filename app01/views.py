#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
# Create your views here.
from models import *

from common.CommonPaginator import SelfPaginator
from common.confhelper import setrole
from common import ldaphelper,confhelper

import os,re
import subprocess

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], 
                            password=request.POST['password'])
        if user:
            if user.is_active:
                login(request,user)  
                return HttpResponseRedirect('/')   
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'app01/login.html', {})



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')  

@login_required
def userlist(request):
    ulist = UserInfo.objects.all()
    data = SelfPaginator(request,ulist, 10)
    ret={'lPage':data}
    return render(request,'app01/userlist.html',ret)

@login_required
def useradd(request):
    ret={'status':None,"groups":None}
    ret['groups']= UserGroup.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username',None)
        name = request.POST.get('realname',None)
        password = request.POST.get('password',None)
        groupId = request.POST.get('group',None)
        email = request.POST.get('email',None)
        is_empty = all([username,name,password,email])
        if is_empty: 
            if groupId == '1':
            #创建SVN帐号和设置权限
                stooge_ou = 'dev'
                l=ldaphelper.LDAPMgmt()
                l.add_stooge(username,stooge_ou,name,email)
            
                c = confhelper.conf("/appdata/Dev/orange5s.authz","groups",stooge_ou)
                c.add_user(username)
            
            else:
            #创建samba帐号
                cmd = '/usr/bin/sudo /usr/bin/ansible -v bjsmb -m shell -a "/usr/local/shell/useradd.sh %s %s"' %(username,password)
                subprocess.call(cmd,shell=True)
        
            groupObj = UserGroup.objects.get(id=groupId)
            UserInfo.objects.create(username=username,
                                    name=name,
                                    password=password,
                                    email=email,
                                    user_type=groupObj)
            
            return redirect('/accounts/userlist/')
        else:
            ret['status']='不能为空.'
    return render(request,'app01/useradd.html',ret)

@login_required
def userdel(request):
    ret={'status':None,"groups":None}
    ret['groups']= UserGroup.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username',None)
        groupId = request.POST.get('group',None)
        if username:
            if groupId == '1':
                #删除SVN帐号
                stooge_ou = 'dev'
                l=ldaphelper.LDAPMgmt()
                l.delete_stooge(username,stooge_ou)
                c = confhelper.conf("/appdata/Dev/orange5s.authz","groups",stooge_ou)
                c.delete_user(username)
            else:
                #删除Samba帐号
                cmd = '/usr/bin/sudo /usr/bin/ansible -v bjsmb -m shell -a "/usr/local/shell/userdel.sh %s"' %(username)
                subprocess.call(cmd,shell=True)
                #删除userlist数据
                UserList.objects.get(username__username=username).delete()
            UserInfo.objects.get(username=username).delete()
            return redirect('/accounts/userlist/')
    return render(request,'app01/userdel.html',ret)



@login_required
def createsvn(request):
    if request.method == 'POST':
        #svnpath = "/appdata/Dev/"
        svname=request.POST.get('svname',None)
        #name = svnpath + str(svname)
        if svname:
            count = Svname.objects.filter(sname=svname).count()
            if count == 1:
                #return svnlist(request)
                return redirect('/accounts/svnlist/')
            else:
                Svname.objects.create(sname=svname)
                Svnversion.objects.create(version=0,
                                          sname=Svname.objects.get(sname=svname)
                                          )
                #插入数据记录
                #os.system("/usr/bin/svnadmin create name")
                #p=subprocess.Popen("sudo /usr/local/shell/create_svn.sh %s" % svname,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                subprocess.call("/usr/bin/sudo /usr/local/shell/create_svn.sh %s" % svname,shell=True)
                return redirect('/accounts/svnlist/')
        
    return render(request,'app01/createsvn.html')

@login_required
def svnlist(request):
    slist = Svname.objects.all()
    data = SelfPaginator(request,slist, 10)
    '''
    for sname in slist:
        n = Svname.objects.get(sname=sname)
        ver=max(n.svnversion_set.values_list('version',flat=True))
        version.append(ver)
        
    svname = Svname.objects.values_list('sname',flat=True)
   
    
    svn_dict = dict(zip(svname,version))
    '''
    ret={'lPage':data}
    return render(request,'app01/svnlist.html',ret)

@login_required
def filelist(request):
   
    ulist = UserList.objects.all()
    data = SelfPaginator(request,ulist, 10)
    ret={'lPage':data}
    
    #print UserList.objects.values('filelist')
    return render(request,'app01/filelist.html',ret)


@login_required
def setfile(request):
    
    ret = {'filelist':None,'roles':None}
    ret['filelist']= FileList.objects.all()
    ret['roles']=FileRole.objects.all()
   
    if request.method == 'POST':
        file_l=[]
        username = request.POST.get('username',None)
        file_id = request.POST.getlist('filel')
        role = request.POST.get('role')
        ulist=UserList.objects.filter(username__username=username)
        usernameObj=UserInfo.objects.get(username=username)
        for i in file_id:
            for j in FileList.objects.filter(id=i):
                file_l.append(j.filename)
        if not ulist:
            if role == '1':
                rfile= ",".join(file_l)
                UserList.objects.create(rfile=rfile,username=usernameObj)
            else:
                wfile= ",".join(file_l)
                UserList.objects.create(wfile=wfile,username=usernameObj)
        else:
            if username and file_l and ulist:
                setrole(role,ulist,file_l)
        
        fileid = " ".join(file_id)
        #cmd = '/usr/bin/sudo /usr/bin/ansible -v bjsmb -m shell -a "/usr/local/shell/setrole.py %s %s %s"' %(role,username,fileid)
        #cmd = "/usr/bin/sudo /usr/local/shell/test.sh %s %s %s" %(role,usernameObj.id,fileid)
        cmd = '/usr/local/shell/setrole.py %s %s %s' %(role,usernameObj.id,fileid)
        subprocess.call(cmd,shell=True)
            
        
        return redirect('/accounts/filelist/')
    
    return render(request,'app01/setfile.html',ret)

@login_required
def webupdate(request):
    return render(request,'app01/webupdate.html')

@login_required
def mysqlupdate(request):
    ret ={"mysqlenv":None,"mysqlname":None}
    ret['mysqlenv']=MysqlEnv.objects.all()
    ret['mysqlname']=Mysqlname.objects.all()
    return render(request,'app01/mysqlupdate.html',ret)