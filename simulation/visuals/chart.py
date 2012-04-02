from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    metric = request.GET.get('metric', '')
    experiment = request.GET.get('experiment','')
    
    if not experiment == "":
        request.session["experiment"] = experiment;
        print 'got new experiment'
    else:
        experiment = request.session["experiment"];
    
    print 'metric is ' + metric
    print 'experiment is ' + experiment
    
    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric,
        'experiment': experiment
    })
    return HttpResponse(t.render(c))