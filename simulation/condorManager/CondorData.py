'''
Created on Feb 29, 2012

The classes in this file represents a condor submission or a 
condor job submitted to Condor. It will store the relevant information
for each condor submission.
@author: songdet
'''


'''
This class represents one Condor submission, consisting of multiple
condor jobs.
'''
class CondorSubmission:
    
    def __init__(self, path, owner, cmd, condorJobs=[]):
        self.path =path
        self.owner = owner
        self.cmd = cmd
        self.condorJobs = condorJobs
    
    def __str__(self):
        retVal = "Path: " + self.path + "\nOwner: " + self.owner + \
                "\nCmd: " + self.cmd + "\n"
        for condorJob in self.condorJobs:
            retVal = retVal + "\n" + str(condorJob) 
        return retVal

#=================================================================#

'''
This class represents a single condor job running by Condor
'''
class CondorJob:
    
    def __init__(self, job_id, args, condor_submission,
                 status='000', status_details='Job submitted'):
        self.job_id = job_id
        self.status = status
        self.status_details = status_details
        self.args = args
        self.condor_submission = condor_submission
    
    def __str__(self):
        return "job_id: " + self.job_id + "\nstatus: " + self.status + \
            "\nstatus_details: " + self.status_details + \
            "\nargs: " + self.args + "\n"

#=================================================================#
