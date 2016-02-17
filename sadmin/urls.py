from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sadmin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', views.index, name ='index'),
    
    url(r'^about/', views.about, name='about'),
    
    url(r'^accounts/', include('app01.urls')),
)
