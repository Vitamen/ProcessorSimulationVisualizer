from django.conf.urls.defaults import patterns, include, url
import os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^config/$', 'experimentManager.views.config'),
    url(r'^config/runExp$', 'experimentManager.views.runExp'),
    url(r'^config/updateArgs$', 'experimentManger.view.updateArgs'),
    url(r'^config/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': os.path.join(PROJECT_PATH,'template')} ),
   
    #url(r'^track/$', 'condorManager.views.tracking'),
    #url(r'^track/endPoint/', 'condorManager.views.endPoint'),
    # url(r'^track/(?P<path>.*)$', 'django.views.static.serve', 
    #  {'document_root': os.path.join(PROJECT_PATH,'condorManager/template')} ),
)
