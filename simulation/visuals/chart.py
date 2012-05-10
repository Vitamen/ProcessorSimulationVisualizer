from django.template import Context, loader
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
    request.session["experiments"] = []
    metric = ''
    benchmarks = []
    benchmarks_selected = []
    all_experiments = ['100M_np_base', '100M_stream_newsys_effra_fp'];
    
    chart_type = 'NOPLOT';
    experiments = [];
    if request.method == 'POST':
        benchmarks_selected = request.POST.getlist('benchmarks')
        experiments = request.POST.getlist('experiments')
        chart_type = request.POST['metric_type']
        metric = request.POST['metric']
        data_root = os.path.join(PROJECT_PATH, "static_media")
        data_root = os.path.join(data_root, "data")
        for i in range(0, len(all_experiments)):
            experiment = all_experiments[i]
            if not os.path.exists(data_root + experiment + os.sep + metric):
                parser.extractMetricFromExperiment(experiment, metric)
    
    parser.extractMetricFromExperiment("100M_np_base", "cycles") 
    t = loader.get_template('visuals/index.html')
    c = Context({
        'chart_type': chart_type,
        'metric': metric,
        'benchmarks_selected': benchmarks_selected,
        'experiments': all_experiments,
        'experiments_selected': experiments
    })
    return HttpResponse(t.render(c))
