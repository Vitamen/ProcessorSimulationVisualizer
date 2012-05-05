from django.http import HttpResponse
from django.template import Context,loader, RequestContext
from datetime import datetime
from models import BenchmarkSuite, Benchmarks, Arguments, \
 ArgumentSet, ArgMembership, Experiments
import re, os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

#########################################################
# Generate the page for an experiment configuration
#########################################################
def config(request):
    # Get the list of benchmarks associated with each suite
    speccpu = Benchmarks.objects.filter(suite = 1)
    spec2006 = Benchmarks.objects.filter(suite = 2)
    
    #load page
    t = loader.get_template("experimentManager/config.html")
    c = Context({
                 'speccpu' : speccpu,
                 'spec2006' : spec2006
            })
    return HttpResponse(t.render(c))

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
    mysubdate = datetime.now()
    experiment = Experiments(expname=myexpname, execpath=myexecpath, bsuite=mybsuite, argset=myargset, subdate=mysubdate)
    experiment.save()
    
    #Generate dictionary of things used in sampleout.html
    t = loader.get_template("experimentManager/sampleoutput.html")
    c = Context({
            'expname' : myexpname,
            'execpath' : myexecpath,
            'bsuite' : request.POST['benchsuite'],
            'paramvaldict' : paramvaldict,
            'speccpu' : speccpu
            })
    return HttpResponse(t.render(c))

#########################################################
# Browse data in the database
#########################################################
def browse(request):
    #Get the list of all experiments in the database
    experiments = Experiments.objects.all() 
    t = loader.get_template("experimentManager/expbrowse.html")
    c = RequestContext( request,
                        {'experiments' : experiments})
    return HttpResponse(t.render(c))
