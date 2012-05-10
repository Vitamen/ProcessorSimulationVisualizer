from django.template import Context, loader
from django.http import HttpResponse
from experimentManager.models import *

def index(request):
    t = loader.get_template('metrics/metrics.html')
    metric_objects = Metric.objects.all()
    metrics = []
    for metric_object in metric_objects:
        metric_item = {"metricname" : metric_object.metricname, 
                       "metrictype" : metric_object.metrictype }
        metrics.append(metric_item)
    c = Context({
                 "metrics": metrics
    })
    return HttpResponse(t.render(c))

def getMetricsOfTypeForExperiments(request):
    experiments = request.POST.getlist('experiments')
    print "got experiments"
    print experiments
    metricType = request.POST.get('metric_type')
    print "of type: "+ metricType
    metricMap = {}
    for experiment in experiments:
        experimentMetric_objects = ExperimentMetric.objects.filter(expname=experiment, metricname__metrictype=metricType)
        print experiment
        for experimentMetric in experimentMetric_objects:
            metric = experimentMetric.metricname
            print metric.metricname
            if metric in metricMap:
                metricMap[metric] = metricMap[metric]+1
            else:
                metricMap[metric] = 1
    
    metrics = [];
    experimentCount = len(experiments)
    for metric in metricMap:
        if metricMap[metric] == experimentCount:
            metrics.append(metric.metricname)
    
    print metrics
    #if len(experiments) == 0 :
    #    metrics = []
    c = Context({
        'metrics': metrics
    })
    return HttpResponse(c)

def updateMetricType(request):
    metric_id = request.POST.get('metric_id')
    metric_type = request.POST.get('metric_type')
    metrics = Metric.objects.filter(metricname=metric_id)
    for metric in metrics:
        metric.metrictype = metric_type
        metric.save()
    return HttpResponse({}) 
