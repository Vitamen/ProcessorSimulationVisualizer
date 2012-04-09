from django.template import Context, loader
from django.http import HttpResponse
from dataParser import parser
import os

def index(request):
    print "here"
    metric = request.GET.get('metric', '')
    experiment = request.GET.get('experiment','')
    request.session['dict'] = {};
    request.session.modified = True;

    if (experiment != None) and (not experiment == ""):
        request.session["experiment"] = experiment;
    else:
        experiment = request.session["experiment"];
    
    if not metric == "":
        request.session["metric"] = metric;
    else:
        metric = request.session["metric"];

    experiment = "100M_stream_newsys_effra_fp"
    data_root = '/Users/sophiez/Dropbox/Spring 2012/DataSimulation/ProcessorSimulationVisualizer/simulation/static_media/data/'
    if not os.path.exists(data_root + experiment + '/' + metric):
        parser.extract(experiment, metric)
    
    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric,
        'experiment': experiment
    })
    return HttpResponse(t.render(c))