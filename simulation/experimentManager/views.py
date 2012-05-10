from django.http import HttpResponse
from django.template import Context,loader, RequestContext
from datetime import datetime
from models import *
import re, os, generator
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
    
    #load page
    t = loader.get_template("experimentManager/config.html")
    binFile = BinRevForms()
    c = Context({
                 'expName' : expName,
                 'speccpu' : speccpu,
                 'spec2006' : spec2006,
                 'baseExp' : baseExp,
                 'extExp' : extExp,
                 'binFile' : binFile
            })
    return HttpResponse(t.render(c))

#########################################################
# Generate the page for an experiment configuration
#########################################################
def runExp(request):
    
    #Use the generator to generate condor.sub and setup
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