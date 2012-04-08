from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    metric = request.GET.get('metric', '')
    #experiment = request.GET.get('experiment','')
    request.session['dict'] = {};
    request.session.modified = True;
    
#    if not experiment == "":
#        request.session["experiment"] = experiment;
#    else:
#        experiment = request.session["experiment"];
    
    if not metric == "":
        request.session["metric"] = metric;
    else:
        metric = request.session["metric"];

    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric,
    #    'experiment': experiment
    })
    return HttpResponse(t.render(c))