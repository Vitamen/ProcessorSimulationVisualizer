from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from experimentManager.models import *
from dataParser import parser
from simulation.settings import PROJECT_PATH
import os.path

def getBenchmarksFromExperiments(request):
    experiments = request.POST.getlist("experiments")
    benchmarkMap = {}
    for experiment in experiments:
        print experiment
        experimentBenchmarks = ExperimentBenchmark.objects.filter(expname__expname=experiment)
        for benchmark in experimentBenchmarks:
            if benchmark.bmname.name in benchmarkMap:
                benchmarkMap[benchmark.bmname.name] = benchmarkMap[benchmark.bmname.name]+1
            else:
                benchmarkMap[benchmark.bmname.name] = 1
        
    benchmarks = [];
    experimentCount = len(experiments)
    for benchmark in benchmarkMap:
        if benchmarkMap[benchmark] == experimentCount:
            benchmarks.append(benchmark)
    
    print benchmarks
    c = Context({
        'benchmarks': benchmarks
    })
    return HttpResponse(c)

def index(request):
     #Get the list of all experiments in the database
    experiments = Experiments.objects.all() 
    
    #Set up the context and page to return
    c = RequestContext(request ,{
        'experiments': experiments,
        'experiments_selected': experiments
    })
    t = loader.get_template('visuals/index.html')
    return HttpResponse(t.render(c))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
