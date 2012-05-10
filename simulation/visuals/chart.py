from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from experimentManager.models import *
from dataParser import parser
from settings import PROJECT_PATH
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
    parser.parseExperiment('100M_stream_newsys_effra_fp');
    request.session["experiments"] = []
    chart_type = 'NOPLOT';
    metric = ''
    benchmarks = []
    benchmarks_selected = []
    all_experiments = ['100M_np_base', '100M_stream_newsys_effra_fp'];
    experiments_selected = []
    
    if request.method == 'POST':
        #get the post data
        chart_type = request.POST['metric_type']
        metric = request.POST['metric']
        benchmarks_selected = request.POST.getlist('benchmarks')
        experiments_selected = request.POST.getlist('experiments')
        
        # parse metrics as necessary
        data_root = os.path.join(PROJECT_PATH, "static_media")
        data_root = os.path.join(data_root, "data")
        for i in range(0, len(experiments_selected)):
            experiment = experiments_selected[i]
            parser.extractMetricFromExperiment(experiment, metric)
    
    t = loader.get_template('visuals/index.html')
    c = Context({
        'chart_type': chart_type,
        'metric': metric,
        'benchmarks_selected': benchmarks_selected,
        'experiments': all_experiments,
        'experiments_selected': experiments_selected
    })
    t = loader.get_template('visuals/index.html')
    return HttpResponse(t.render(c))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
