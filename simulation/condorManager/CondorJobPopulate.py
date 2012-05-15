import shlex, sys
from simulation.condorManager.models import CondorJob
    
'''
    Populate list of condorJobs with jobs
'''
def populateJobs(msg):
    #Check and cut message to relevant part
    if len(msg) == 0: return
    
    #Go through each line, create a job for each line and populate
    lines = __processMsg(msg)
    for line in lines:
        splitVal = shlex.split(line)
        curJob = CondorJob(job_id=splitVal[0],
                        submitted=splitVal[2]+splitVal[3],
                        run_time=splitVal[4],
                        st=splitVal[5], 
                        pri=splitVal[6], 
                        size=splitVal[7],
                        cmd=splitVal[8])
        curJob.save()
        
            
            
#=================================================================#

'''
    Delete all jobs in CondorJob table
'''
def deleteJobs():
    CondorJob.objects.all().delete()
    
#=================================================================#

'''
    Delete specified job from table
'''
def deleteJob(myId):
    CondorJob.objects.get(job_id=myId).delete()
    
#=================================================================#
'''
    Update job
'''
def updateStopJob(myId):
    val = CondorJob.objects.get(job_id=myId)
    val.st = "X"
    val.save()
    return val
    
#=================================================================#
'''
    Check if the status has been updated. If status is updated,
    update
'''
def checkUpdate(msg):
    #Process the current status message into dictionaries
    curJobs = {}
    if len(msg) == 0: return
    lines = __processMsg(msg)
    for line in lines:
        splitVal = shlex.split(line)
        curJobs[splitVal[0]] =  [splitVal[0],  splitVal[2]+splitVal[3], 
                                splitVal[4], splitVal[5], splitVal[6],
                                splitVal[7], splitVal[8]]
    
    #Iterate through the dict of current jobs and compare to
    #see if anything has changed. If it is, call socket update
    changedJobs = []
    allJobs = CondorJob.objects.all()
    for job in allJobs:
        #If the current id is not in current job, it must be completed
        #Remove from condorJobs and append finished job to changedJobs
        if job.job_id not in curJobs and job.st != "C" and job.st != "X":
            job.st = "C"
            job.save()
            changedJobs.append(job)
        #Check for changed st and add to those that change
        elif job.job_id in curJobs and job.st != curJobs[job.job_id][3]:
            job.run_time = curJobs[job.job_id][2]
            job.st = curJobs[job.job_id][3]
            job.pri = curJobs[job.job_id][4]
            job.save()
            changedJobs.append(curJobs[job.job_id])
    return changedJobs

#=================================================================#

def __processMsg(msg):
    msg = msg[msg.index(" CMD")+4:].strip()
    lines = msg.split("\n")
    if len(lines) != 0: lines = lines[:-1]
    lines = map(str.strip,lines)
    retLine = []
    for line in lines:
        if line != "": retLine.append(line)
    return retLine

#=================================================================#
