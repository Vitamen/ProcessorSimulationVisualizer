from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
import re, json, os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
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
    #Create argument set for this experiment set
    myargset = ArgumentSet(setname=request.POST['expname'])
    myargset.save()
    
    #Create arguments and save to argument set
    paramx = re.compile('param([\d_]+)')
    valx = re.compile("^val([\d_]+)")
    paramdict = {}
    valdict = {}
    paramvaldict = {}
    speccpu = Benchmarks.objects.filter(suite = 1)
    
    for curVal in request.POST:
        if re.match(paramx, curVal):
            numArg = paramx.search(curVal).group(1)
            paramdict[numArg] = request.POST[curVal]
        elif re.match(valx, curVal):
            numArg = valx.search(curVal).group(1)
            valdict[numArg] = request.POST[curVal]
    for curVal in paramdict:
        p = Arguments(argname=paramdict[curVal], value=valdict[curVal])
        paramvaldict[paramdict[curVal]] = valdict[curVal]
        p.save()
        argmember = ArgMembership(setname=myargset,argname=p)
        argmember.save()
    
    #Create experiment and save to list
    myexpname = request.POST['expname']
    myexecpath = request.POST['path']
    mybsuite = BenchmarkSuite.objects.get(suite=request.POST['benchsuite'])
    experiment = Experiments(expname=myexpname, execpath=myexecpath, bsuite=mybsuite, argset=myargset)
    experiment.save()
    
    #Generate dictionary of things used in sampleout.html
    dict = {
            'expname' : myexpname,
            'execpath' : myexecpath,
            'bsuite' : request.POST['benchsuite'],
            'paramvaldict' : paramvaldict,
            'speccpu' : speccpu
            }
    return render_to_response('sampleoutput.html', dict, context_instance=RequestContext(request))
        