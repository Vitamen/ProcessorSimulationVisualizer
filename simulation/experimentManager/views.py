from django.http import HttpResponse
from django.template import Context,loader, RequestContext
from datetime import datetime
from models import BenchmarkSuite, Benchmarks, Arguments, \
 ArgumentSet, ArgMembership, Experiments
import re, os, generator

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
    curArgSet = ArgumentSet(setname=request.POST['expname'])
    curArgSet.save()
    
    #Create arguments and save to argument set
    paramx = re.compile('param([\d_]+)')
    valx = re.compile("^val([\d_]+)")
    paramdict = {}
    valdict = {}
    paramvaldict = {}
    
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
        argmember = ArgMembership(setname=curArgSet,argname=p)
        argmember.save()
    
    #Create experiment and save to list
    myexpname = request.POST['expname']
    myexecpath = request.POST['path']
    mybsuite = BenchmarkSuite.objects.get(suite=request.POST['benchsuite'])
    mysubdate = datetime.now()
    experiment = Experiments(expname=myexpname, execpath=myexecpath, bsuite=mybsuite, argset=myargset, subdate=mysubdate)
    experiment.save()
    
    #Check additional settings and create context
    #Call generator to start an experiment
    '''useOut = request.POST.has_key('useOut')
    useErr = request.POST.has_key('useErr')
    useLog = request.POST.has_key('useLog')
    exclBench = request.POST['as_values_1']
    experimentVal = {
        'useOut' : useOut,
        'useErr' : useErr,
        'useLog' : useLog,
        'expname' : myexpname,
        'execpath' : myexecpath,
        'bsuite' : request.POST['benchsuite'],
        'exclBench' : exclBench, 
        'paramvaldict' : paramvaldict,
        
        }'''
    generator.generate(request)
    
    
    #Generate dictionary of things used in sampleout.html
    c = Context()  
    t = loader.get_template("experimentManager/sampleoutput.html")
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
