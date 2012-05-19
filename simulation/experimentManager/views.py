from django.http import HttpResponse
from django.template import Context,loader, RequestContext
from simulation.condorManager.CondorManager import Manager
from simulation.condorManager.models import CondorJob
from simulation.settings import EXP_ROOT_DIR
from datetime import datetime
from models import *
import re, os, generator, sys
from django.core import serializers

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

#########################################################
# Generate the page for an experiment configuration
#########################################################
def config(request):
    # Get the list of benchmarks associated with each suite
    speccpu = Benchmarks.objects.filter(suite = 1)
    spec2006 = Benchmarks.objects.filter(suite = 2)
    baseExp = BaseExperiment.objects.all()
    extExp = ExtExperiment.objects.all()
    expName = generator.decideName()
    sizepref = DefaultValues.objects.get(name='size_pref').value
    size = DefaultValues.objects.get(name='size').value
    common = DefaultValues.objects.get(name='common').value
    binFile = BinRevForms()
    
    #load page
    retDict = {
                 'expName' : expName,
                 'speccpu' : speccpu,
                 'spec2006' : spec2006,
                 'baseExp' : baseExp,
                 'extExp' : extExp,
                 'binFile' : binFile,
                 'sizepref' : sizepref,
                 'size' : size,
                 'common' : common,
            }
    t = loader.get_template("experimentManager/config.html")
    c = Context(retDict)
    return HttpResponse(t.render(c))

#########################################################
# Generate the page for an experiment configuration
#########################################################
def runExp(request):
    
    #Use the generator to generate condor.sub and setup
    #relevant directories
    condorFile = generator.generate(request)

    #Start job and return success
    condorFile = os.path.join(EXP_ROOT_DIR,"tmp","condor.sub")
    manage = Manager()
    manage.startJob(condorFile)
    return HttpResponse("Success!")
    
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
# Get the page for setting default values
#########################################################
def setDefault(request):
    common = DefaultValues.objects.filter(name="common")
    size_pref = DefaultValues.objects.filter(name="size_pref")
    size = DefaultValues.objects.filter(name="size")
    baseExp = DefaultValues.objects.filter(name="baseExp")
    extExp = DefaultValues.objects.filter(name="extExp")
    
    print >>sys.stderr, common
    if len(common) == 0: 
        common = DefaultValues(name="common", value="null")
        common.save()
    else:
        common = common[0]
    if len(size_pref) == 0: 
        size_pref = DefaultValues(name="size_pref", value="null")
        size_pref.save()
    else: 
        size_pref = size_pref[0]
    if len(size) == 0: 
        size = DefaultValues(name="size", value="null")
        size.save()
    else: 
        size = size[0]
    if len(baseExp) == 0:
        baseExp = DefaultValues(name="baseExp", value="np : -pref false")
        baseExp.save()
    else:
        baseExp = baseExp[0]
    if len(extExp) == 0:
        extExp = DefaultValues(name="extExp", value="effra_overlap0.5 : eff-core_ra_efficient true -core_ra_efficient_overlap_T 0.5")
        extExp.save()
    else:
        extExp = extExp[0]
    c = Context({
                    'common' : common,
                    'size_pref' : size_pref,
                    'size' : size,
                    'baseExp' : baseExp,
                    'extExp' : extExp
                 })  
    t = loader.get_template("experimentManager/setDefault.html")
    return HttpResponse(t.render(c))

#########################################################
# Update default values
#########################################################
def updateDefault(request):
    #If this is a refresh, simply return the page
    if len(request.POST) == 0 : return setDefault(request)
    
    #update values in the database for default values
    retDict = updateValues(request)
    
    #Clear models for base and extended experiment and
    #insert new ones
    BaseExperiment.objects.all().delete()
    ExtExperiment.objects.all().delete()
    parseBaseAndExt(request.POST['baseExp'], 'base')
    parseBaseAndExt(request.POST['extExp'], 'ext')
    c = Context(retDict)  
    t = loader.get_template("experimentManager/setDefault.html")
    return HttpResponse(t.render(c))

#########################################################
# Update values from database
#########################################################
def updateValues(request):
    postMap = request.POST
    retDict = {}
    for key in postMap:
        curArg = postMap[key].strip()
        databaseArg = DefaultValues.objects.get(name=key)
        databaseArg.value = curArg
        databaseArg.save()
        retDict[key] = databaseArg
    return retDict

#########################################################
# Update values in database
#########################################################
def parseBaseAndExt(exp, expType):
    lines = exp.split("\n")
    for line in lines:
        if line == "" : continue
        curArgs = line.split(" : ")
        if expType == "base":
            curBase = BaseExperiment(name=curArgs[0], value=curArgs[1])
            curBase.save()
        elif expType == "ext":
            curExt = ExtExperiment(name=curArgs[0], value=curArgs[1])
            curExt.save()
