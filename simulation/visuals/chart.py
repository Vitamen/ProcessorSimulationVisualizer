from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    metric = request.GET.get('metric', '')
    print 'metric is ' + metric
    t = loader.get_template('visuals/index.html')
    c = Context({
        'metric': metric
    })
    return HttpResponse(t.render(c))