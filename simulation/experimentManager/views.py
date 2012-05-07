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
    
    #RegEx for recognizing arguments
    paramx = re.compile('param([\d_]+)')
    valx = re.compile("^val([\d_]+)")
    
    #Create experiment and save to list
    baseExpName = request.POST['size_pref']
    expTypes = [x.strip() for x in request.POST["as_values_2"].split(",")]
    for expType in expTypes:
        if expType == "" : continue
        myexpName = request.POST['expname'] + baseExpName + expType
        
        '''#Create argset
        curArgSet = ArgumentSet(setname=myexpName)
        curArgSet.save()'''
        
        #Create argument set for this experiment set
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
        '''for curVal in paramdict:
            p = Arguments(argname=paramdict[curVal], value=valdict[curVal])
            paramvaldict[paramdict[curVal]] = valdict[curVal]
            p.save()
            argmember = ArgMembership(setname=curArgSet,argname=p)
            argmember.save()'''
        experiment = Experiments(expname=myexpName, execpath="",
                                bsuite=BenchmarkSuite.objects.get(suite=request.POST['benchsuite']), 
                                subdate= datetime.now())
        experiment.save()
    
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

#########################################################
# Get the static page for Condor
#########################################################
def getCondor(request):
    c = Context()  
    t = loader.get_template("experimentManager/sampleoutput.html")
    return HttpResponse(t.render(c))