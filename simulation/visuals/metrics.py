from django.template import Context, loader
from django.http import HttpResponse
from simulation.experimentManager.models import *
from simulation.dataParser.parser import parseExperiment, extractMetricFromExperiment

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
    #Get submission name and experiment name needed
    expName = request.POST['expName'][:-1]
    expName = sepByComma(expName)
    subName = request.POST['subName'][:-1]
    subName = sepByComma(subName)
    print "got experiments"
    print expName, subName
    
    #Get metric type
    metricType = request.POST.get('metric_type')
    print "of type: "+ metricType
    metricMap = {}
    
    #Iterate through all selected experiments
    for i in range(0, len(expName)):
        #Use parser to parse selected experiment
        curSub = subName[i]
        curExp = expName[i]
        experiment_object = Experiments.objects.get(submissionName=curSub, expName=curExp)
        parseExperiment(curSub,curExp, metricType)
        
        #Get out metrics this experiment
        experimentMetric_objects = ExperimentMetric.objects.filter(expname=experiment_object.pk, metricname__metrictype=metricType)
        print len(experimentMetric_objects)
        for experimentMetric in experimentMetric_objects:
            metric = experimentMetric.metricname
            if metric in metricMap:
                metricMap[metric] = metricMap[metric]+1
            else:
                metricMap[metric] = 1 
    
    metrics = [];
    experimentCount = len(expName)
    for metric in metricMap:
        if metricMap[metric] == experimentCount:
            metrics.append(metric.metricname)
    
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

def sepByComma(value):
    return [x.strip() for x in value.split(",")]
