from django.template import Context, loader
from django.http import HttpResponse
from experimentManager.models import *
from dataParser import parser
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
    all_experiments = ['100M_np_base', '100M_stream_newsys_effra_fp'];

    data_root = '/Users/sophiez/Dropbox/Spring 2012/DataSimulation/ProcessorSimulationVisualizer/simulation/static_media/data/'
    
    experiments = [];
    if request.method == 'POST':
        benchmarks = request.POST.getlist('benchmarks')
        experiments = request.POST.getlist('experiments')
        metric = request.POST['metric']
        print benchmarks
        print experiments
        print metric
    
    for i in range(0, len(all_experiments)):
        experiment = all_experiments[i]
        if not os.path.exists(data_root + experiment + '/' + metric):
            parser.extractMetricFromExperiment(experiment, metric)

    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric,
        'benchmarks': benchmarks,
        'experiments': all_experiments,
        'experiments_selected': experiments
    })
    return HttpResponse(t.render(c))
