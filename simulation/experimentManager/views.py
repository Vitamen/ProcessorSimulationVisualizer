from django.http import HttpResponse
from django.template import Context,loader, RequestContext
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
    baseExp = BaseExperimentTypes.objects.all()
    extExp = ExtendedExperimentTypes.objects.all()
    expName = generator.decideName()
    sizepref = DefaultValues.objects.get(name='size_pref').value
    size = DefaultValues.objects.get(name='size').value
    common = DefaultValues.objects.get(name='common').value
    #load page
    t = loader.get_template("experimentManager/config.html")
    binFile = BinRevForms()
    c = Context({
                 'expName' : expName,
                 'speccpu' : speccpu,
                 'spec2006' : spec2006,
                 'baseExp' : baseExp,
                 'extExp' : extExp,
                 'binFile' : binFile,
                 'sizepref' : sizepref,
                 'size' : size,
                 'common' : common,
            })
    return HttpResponse(t.render(c))

#########################################################
# Generate the page for an experiment configuration
#########################################################
def runExp(request):
    
    #Use the generator to generate condor.sub anBd setup
    #relevant directories
    generator.generate(request)
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
# Get the static page for Condor
#########################################################
def getCondor(request):
    c = Context()  
    t = loader.get_template("experimentManager/sampleoutput.html")
    return HttpResponse(t.render(c))

#########################################################
# Get the page for setting default values
#########################################################
def setDefault(request):
    common = DefaultValues.objects.filter(name="common")
    size_pref = DefaultValues.objects.filter(name="size_pref")
    size = DefaultValues.objects.filter(name="size")
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
    c = Context({
                    'common' : common,
                    'size_pref' : size_pref,
                    'size' : size,
                 })  
    t = loader.get_template("experimentManager/setDefault.html")
    return HttpResponse(t.render(c))

#########################################################
# Update default values
#########################################################
def updateDefault(request):
    common = request.POST['common']
    common = common.strip()
    commonUpdate = DefaultValues.objects.get(name="common")
    commonUpdate.value = common
    commonUpdate.save()
    size_pref = request.POST['size_pref']
    size_prefUpdate = DefaultValues.objects.get(name="size_pref")
    size_prefUpdate.value = size_pref
    size_prefUpdate.save()
    size = request.POST['size']
    sizeUpdate = DefaultValues.objects.get(name="size")
    sizeUpdate.value = size
    sizeUpdate.save()
    c = Context({
                    'common' : commonUpdate,
                    'size_pref' : size_prefUpdate,
                    'size' : sizeUpdate,
                 })  
    t = loader.get_template("experimentManager/setDefault.html")
    return HttpResponse(t.render(c))