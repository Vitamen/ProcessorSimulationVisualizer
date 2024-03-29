from django.conf.urls.defaults import patterns, include, url
import os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^config/$', 'experimentManager.views.config'),
    url(r'^config/runExp$', 'experimentManager.views.runExp'),
    url(r'^config/updateArgs$', 'experimentManger.view.updateArgs'),
    url(r'^chart/$', 'visuals.chart.index'),
    url(r'^chart/(?P<username>)/$', 'visuals.chart.metric'),
    url(r'^getMetricsForExperiment', 'visuals.metrics.metricsForExperiment'),
    url(r'^getMetricsOfTypeForExperiments', 'visuals.metrics.getMetricsOfTypeForExperiments'),
    url(r'^getBenchmarksFromExperiments', 'visuals.chart.getBenchmarksFromExperiments'),
    url(r'^setUpMetrics', 'visuals.metrics.setUpMetrics'),
    url(r'^updateMetricType', 'visuals.metrics.updateMetricType'),
    url(r'^metrics/$', 'visuals.metrics.index'),
    url(r'^browse/$', 'experimentManager.views.browse'),
    url(r'^setDefault/$', 'experimentManager.views.setDefault'),
    url(r'^updateDefault/$', 'experimentManager.views.updateDefault'),
    url(r'^config/getCondor$', 'condorManager.views.initTable'),
    url(r'^getTableUpdates/$', 'condorManager.views.updateTable'),
    url(r'^handleJobs/$', 'condorManager.views.handleJobs'),
    url(r'^manualParse/$', 'visuals.metrics.manualParse'),
    #Url to read lines from a file
    url(r'^read/$', 'dataParser.parser.readFile'),
    url(r'^listExp/$','dataParser.parser.getExperimentList'),
    url(r'^getData/$','dataParser.parser.getDataFor'),
    url(r'^extractBenchmarks/$', 'dataParser.parser.parseExperiment'),
    url(r'^$', 'experimentManager.views.config'),
)
    # Examples:
    # url(r'^$', 'simulation.views.home', name='home'),
    # url(r'^simulation/', include('simulation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

urlpatterns += patterns('django.views.static',
    (r'^static_media/(?P<path>.*)$', 
        'serve', {
        'document_root':  os.path.join(PROJECT_PATH,'static_media'),
        'show_indexes': True }),)

urlpatterns += patterns('django.views.static',
    (r'^parsedExperiments/(?P<path>.*)$', 
        'serve', {
        'document_root':  os.path.join(PROJECT_PATH,'parsedExperiments'),
        'show_indexes': True }),)
