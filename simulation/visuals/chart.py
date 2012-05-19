from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from simulation.experimentManager.models import *
from simulation.experimentManager import generator
from simulation.dataParser import parser
from simulation.settings import PROJECT_PATH
import os.path

############################################################

def getBenchmarksFromExperiments(request):
    experiments = getExperiments(request)
    benchmarkMap = {}
    for experiment in experiments: 
        #Get experiments benchmarks
        experimentBenchmarks = parser.extractBenchmarksFromExperiments(experiment[0], experiment[1])
        for experimentBenchmark in experimentBenchmarks:
            benchmark = experimentBenchmark.benchmark
            print benchmark.name
            if benchmark.name in benchmarkMap:
                benchmarkMap[benchmark.name] = benchmarkMap[benchmark.name]+1
            else:
                benchmarkMap[benchmark.name] = 1
        
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

############################################################

def index(request):
    
    metric = findOrCreateMetricByName('SampleAggregateMetric', True)
#    metricAggregatesWithText = MetricAggregate.objects.filter(metric = metric);
#    if len(metricAggregatesWithText) == 1:
#        return metricAggregatesWithText[0]
#    elif len(metricAggregatesWithText) == 0:
#        metric = MetricAggregate.objects.create(metric = metric, metrictype='HISTOGRAM', isAggregate = aggregate)
#        return metric
    #Set up default values to pass to index
    request.session["experiments"] = []
    chart_type = 'NOPLOT';
    metric = ''
    benchmarks = []
    benchmarks_selected = []
    experiments = Experiments.objects.all() 
    experiments_selected = []
    experiments_selected_ret = []
    
    #Modify values for refresh pages
    if request.method == 'POST':
        #get the post data
        chart_type = request.POST['metric_type']
        metric = request.POST['metric']
        benchmarks_selected = request.POST.getlist('benchmarks')
        experiments_selected = getExperiments(request)
        experiments_selected_ret = getExperimentsRet(request)
        
        
        # parse metrics as necessary
        for i in range(0, len(experiments_selected)):
            experiment = experiments_selected[i]
            print "subName:" +experiment[0]+";"
            print "expName:"+experiment[1]+";"
            print "metric:"+metric+";"
            parser.extractMetricFromExperiment(experiment[0], experiment[1],metric)
            
            
    #Set up the context and page to return
    c = RequestContext(request ,{
        'chart_type': chart_type,
        'metric': metric,
        'benchmarks_selected': benchmarks_selected,
        'experiments': experiments,
        'experiments_selected': experiments_selected,
        'experiments_selected_ret': experiments_selected_ret,
    })
    t = loader.get_template('visuals/index.html')
    return HttpResponse(t.render(c))


############################################################

def sepByComma(value):
    return [x.strip() for x in value.split(",")]

############################################################

def getExperiments(request):
    subName = request.POST['subName'][:-1]
    subName = sepByComma(subName)
    expName = request.POST['expName'][:-1]
    expName = sepByComma(expName)
    expList = []
    for i in range(0, len(subName)):
        expList.append([subName[i], expName[i]])
    return expList

############################################################

def getExperimentsRet(request):
    expName = request.POST['expName'][:-1]
    expName = sepByComma(expName)
    expList = []
    for i in range(0, len(expName)):
        expList.append(expName[i])
    return expList
############################################################

