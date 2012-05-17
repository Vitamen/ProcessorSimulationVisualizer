from django.http import HttpResponse
from django.template import loader, Context
from CondorManager import Manager
from simulation.condorManager import CondorJobPopulate
from simulation.condorManager.models import CondorJob
from simulation.experimentManager import generator
from simulation.settings import EXP_ROOT_DIR
from django.core import serializers
import sys, os

#=================================================================#

'''
    Show the first page and initialize the table for showing condor status
'''
def initTable(request):
    #Populate the database with current jobs
    manage = Manager()
    retVal = manage.getStatus()
    CondorJobPopulate.populateJobs(retVal)
    
    #Get current running experiment & jobs
    retDict = {'jobs' : CondorJob.objects.all()}
    
    #Return
    c = Context(retDict)  
    t = loader.get_template("condorManager/condorjobs.html")
    return HttpResponse(t.render(c))

#=================================================================#

'''
    Show the first page and initialize the table for showing condor status
'''
def updateTable(request):
    #Use CondorJobPopulat to get updates
    manage = Manager()
    retVal = manage.getStatus()
    changedJobs = CondorJobPopulate.checkUpdate(retVal)
    data = serializers.serialize('json', changedJobs)
    print sys.stderr, data
    return HttpResponse(data, "application/json")

#=================================================================#

'''
    Handle the job passed in
'''
def handleJobs(request):
    if 'stop' in request.POST: changedJobs = stopOrDeleteJob(request, "stop")
    elif 'delete' in request.POST: changedJobs = stopOrDeleteJob(request, "delete")
    elif 'restart' in request.POST: changedJobs = restartJob(request)
    data = serializers.serialize('json', changedJobs)
    return HttpResponse(data, "application/json")
    
#=================================================================#

'''
    Stop or delete the selected job from running and marked as removed
'''
def stopOrDeleteJob(request, jobType):
    manage = Manager()
    jobs = sepByComma(request.POST['subName'])
    changedJobs = []
    for job in jobs:
        job = job.strip()
        if job == "": continue
        if jobType == "stop" : 
            manage.stopJob(job)
            changedJobs.append(CondorJobPopulate.updateStopJob(job))
        elif jobType == "delete" :
            CondorJobPopulate.deleteJob(job)
    return changedJobs


#=================================================================#

'''
    Prepare the selected job for resubmission. Use condor_q -long
    to get required arguments to resubmitt
'''
def restartJob(request):
    jobs = sepByComma(request.POST['subName'])
    changedJobs = []
    for job in jobs:
        job = job.strip()
        if job == "": continue
        generator.makeResubmission(job)
    return changedJobs
#=================================================================#

def sepByComma(value):
    return [x.strip() for x in value.split(",")]

#=================================================================#