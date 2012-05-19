from django.template import Context, loader
from django.http import HttpResponse
from simulation.experimentManager.models import *
from simulation.dataParser.parser import *
from simulation.experimentManager.models import *
import os

def index(request):
    if request.method == 'POST':
        metricName = request.POST['metricName']
        metricType = request.POST['metricType']
        evalString = request.POST['evalString']
        metric, created = Metric.objects.get_or_create(metricname = metricName);
        metric.metrictype = metricType;
        metric.isAggregate = True;
        metric.save()
    
        metricAggregate, created = MetricAggregate.objects.get_or_create(metric = metric)
        metricAggregate.evalString = evalString
        metricAggregate.save()

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
    experiments = request.POST['expName'][:-1]
    experiments = sepByComma(experiments)
    subName = request.POST['subName'][:-1]
    subName = sepByComma(subName)
    
    #Get metric type
    metricType = request.POST.get('metric_type')
    metricMap = {}
    
    #Iterate through all selected experiments
    for i in range(0, len(experiments)):
        #Use parser to parse selected experiment
        curSub = subName[i]
        curExp = experiments[i]
        experiment_object = Experiments.objects.get(submissionName=curSub, expName=curExp)
        parseExperiment(curSub,curExp)
        
        #Get out metrics this experiment
        experimentMetric_objects = ExperimentMetric.objects.filter(expname=experiment_object.pk, metricname__metrictype=metricType)
        for experimentMetric in experimentMetric_objects:
            metric = experimentMetric.metricname
            if metric in metricMap:
                metricMap[metric] = metricMap[metric]+1
            else:
                metricMap[metric] = 1 
    
    metrics = [];
    experimentCount = len(experiments)
    print experimentCount
    for metric in metricMap:
        if metricMap[metric] == experimentCount:
            metrics.append(metric.metricname)
            
    #Add additional aggregate metrics
    metric_objects = Metric.objects.filter(isAggregate=True)
    print metric_objects
    for metric in metric_objects:
        print metric
        metrics.append(metric.metricname)

    metrics = sorted(metrics)
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

def manualParse(request):
    #Get values of POST
    if request.method == 'POST':
        subName = request.POST['subName']
        expName = request.POST['expName']

        #Check that the folders exist and parse experiment
        pathCheck = os.path.join(subName,expName)
        if not os.path.exists(pathCheck):
            print "ERROR: path does not exist"
            return
        
        parseExperimentWithRootDirectory(pathCheck)
    t = loader.get_template("visuals/manparse.html")
    c = Context()
    return HttpResponse(t.render(c))

def sepByComma(value):
    return [x.strip() for x in value.split(",")]
