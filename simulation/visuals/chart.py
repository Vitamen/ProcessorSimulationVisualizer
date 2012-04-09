from django.template import Context, loader
from django.http import HttpResponse
from dataParser import parser
import os
import array

def index(request):
    request.session["experiments"] = []
    metric = request.GET.get('metric', '')
    experiment = request.GET.get('experiment','')
    request.session.modified = True;

    if (experiment != None) and (not experiment == ""):
        request.session["experiments"].append(experiment)
        request.session.modified = True
        experiments = request.session["experiments"]
    else:
        experiments = request.session["experiments"]
    
    if not metric == "":
        request.session["metric"] = metric;
    else:
        metric = request.session["metric"];

    data_root = '/Users/sophiez/Dropbox/Spring 2012/DataSimulation/ProcessorSimulationVisualizer/simulation/static_media/data/'
            
    for i in range(0, len(experiments)):
        experiment = experiments[i]
        if not os.path.exists(data_root + experiment + '/' + metric):
            parser.extract(experiment, metric)
        
    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric,
        'experiments': experiments
    })
    return HttpResponse(t.render(c))
