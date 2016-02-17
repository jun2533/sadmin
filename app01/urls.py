from django.conf.urls import patterns, include, url

from app01 import views

urlpatterns = patterns('',
  
    
    #url(r'^login/', views.login),
    #url(r'^index/', views.index),
    #url(r'^register/', views.register),
    #url(r'^host/', views.addhost),
    #url(r'^ajax/', views.ajax),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^userlist/', views.userlist, name='userlist'),
    url(r'^useradd/', views.useradd, name='useradd'),
    url(r'^createsvn/', views.createsvn, name='createsvn'),
    url(r'^svnlist/', views.svnlist, name='svnlist'),
)
