#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
# Create your views here.
from models import UserInfo,UserGroup,Svname,Svnversion,MysqlEnv,Mysqlname

from common.CommonPaginator import SelfPaginator
import os
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
    data = SelfPaginator(request,ulist, 8)
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
        #print is_empty
        if groupId == '1':
            
            print "OK"
        else:
            print "NO"
        if is_empty:
            groupObj = UserGroup.objects.get(id=groupId)
            
            UserInfo.objects.create(username=username,
                                    name=name,
                                    password=password,
                                    email=email,
                                    user_type=groupObj)           
            return userlist(request)
        else:
            ret['status']='不能为空.'
    return render(request,'app01/useradd.html',ret)

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
                #插入数据记录
                #os.system("/usr/bin/svnadmin create name")
                subprocess.call("sudo /usr/local/shell/create_svn.sh %s" % svname,shell=True)
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
def webupdate(request):
    return render(request,'app01/webupdate.html')

@login_required
def mysqlupdate(request):
    ret ={"mysqlenv":None,"mysqlname":None}
    ret['mysqlenv']=MysqlEnv.objects.all()
    ret['mysqlname']=Mysqlname.objects.all()
    return render(request,'app01/mysqlupdate.html',ret)