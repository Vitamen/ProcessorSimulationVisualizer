from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^chart/$', 'visuals.chart.index'),
    url(r'^chart/(?P<username>)/$', 'visuals.chart.metric'),
    
    #Url to read lines from a file
    url(r'^read/$', 'dataParser.parser.readFile'),
    url(r'^listExp/$','dataParser.parser.getExperimentList'),
    url(r'^getData/$','dataParser.parser.getDataFor')
    
    # Examples:
    # url(r'^$', 'simulation.views.home', name='home'),
    # url(r'^simulation/', include('simulation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.views.static',
    (r'^static_media/(?P<path>.*)$', 
        'serve', {
        'document_root': '/Users/sophiez/Dropbox/Spring 2012/DataSimulation/ProcessorSimulationVisualizer/simulation/static_media',
        'show_indexes': True }),)
    