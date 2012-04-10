from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
import re

#########################################################
# Generate the page for an experiment configuration
#########################################################
def config(request):
    # Get the list of benchmarks associated with each suite
    speccpu = Benchmarks.objects.filter(suite = 1)
    spec2006 = Benchmarks.objects.filter(suite = 2)
    
    #load page
    dict = {
                 'speccpu' : speccpu,
                 'spec2006' : spec2006
            }
    return render_to_response('config.html', dict, context_instance=RequestContext(request))

#########################################################
# Generate the page for an experiment configuration
#########################################################
def runExp(request):
    #Store experimental details in the database
    expname = request.POST['expname']
    execPath = request.POST['path']
    bsuite = request.POST['benchsuite']
    paramx = re.compile('param([\d_]+)')
    valx = re.compile("^val([\d_]+)")
    paramdict = {}
    valdict = {}
    for curVal in request.POST:
        if re.match(paramx, curVal):
            numArg = paramx.search(curVal).group(1)
            paramdict.update(numArg, request.POST[curVal])
        elif re.match(valx, curVal):
            numArg = valx.search(curVal).group(1)
            valdict.update(numArg, request.POST[curVal])
    return render_to_response('sampleoutput.html', dict, context_instance=RequestContext(request))
 
    
    