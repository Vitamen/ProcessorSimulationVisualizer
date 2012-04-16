from django.template import Context, loader
from django.http import HttpResponse
from dataParser import parser
import os

def index(request):
    request.session["experiments"] = []
    metric = ''
    benchmarks = []
    speccpu=[
    "00.ammp", 
    "00.applu", 
    "00.art", 
    "00.equake", 
    "00.facerec", 
    "00.lucas", 
    "00.mcf", 
    "00.mgrid", 
    "00.parser", 
    "00.swim", 
    "06.2.400.perlbench", 
    "06.2.401.bzip2", 
    "06.2.403.gcc", 
    "06.2.410.bwaves", 
    "06.2.416.gamess", 
    "06.2.429.mcf", 
    "06.2.433.milc", 
    "06.2.434.zeusmp", 
    "06.2.435.gromacs", 
    "06.2.436.cactusADM", 
    "06.2.437.leslie3d", 
    "06.2.444.namd", 
    "06.2.445.gobmk", 
    "06.2.447.dealII", 
    "06.2.450.soplex", 
    "06.2.453.povray", 
    "06.2.454.calculix", 
    "06.2.456.hmmer", 
    "06.2.458.sjeng", 
    "06.2.459.GemsFDTD", 
    "06.2.462.libquantum", 
    "06.2.464.h264ref", 
    "06.2.465.tonto", 
    "06.2.470.lbm", 
    "06.2.471.omnetpp", 
    "06.2.473.astar", 
    "06.2.482.sphinx3", 
    "06.400.perlbench", 
    "06.401.bzip2", 
    "06.403.gcc", 
    "06.410.bwaves", 
    "06.416.gamess", 
    "06.429.mcf", 
    "06.433.milc", 
    "06.434.zeusmp", 
    "06.435.gromacs", 
    "06.436.cactusADM", 
    "06.437.leslie3d"         
    ]
    all_experiments = ['100M_np_base', '100M_stream_newsys_effra_fp'];

    data_root = '/Users/sophiez/Dropbox/Spring 2012/DataSimulation/ProcessorSimulationVisualizer/simulation/static_media/data/'
    
    experiments = [];
    if request.method == 'POST':
        benchmarks = request.POST.getlist('benchmarks')
        experiments = request.POST.getlist('experiments')
        metric = request.POST['metric']
    
    for i in range(0, len(all_experiments)):
        experiment = all_experiments[i]
        #if not os.path.exists(data_root + experiment + '/' + metric):
        #    parser.extract(experiment, metric)

    t = loader.get_template('visuals/index.html')
    c = Context({
        'speccpu' : speccpu,
        'metric': metric,
        'benchmarks': benchmarks,
        'experiments': all_experiments,
        'experiments_selected': experiments
    })
    return HttpResponse(t.render(c))
