'''
Created on Feb 29, 2012

@author: songdet
'''

class CondorSubmission:
    
    def __init__(self, path, owner, cmd, condorJobs=[]):
        self.path =path
        self.owner = owner
        self.cmd = cmd
        self.condorJobs = condorJobs

#=================================================================#

class CondorJob:
    
    def __init__(self, job_id, args, condor_submission,
                 status='000', status_details='Job submitted'):
        self.job_id = job_id
        self.status = status
        self.status_details = status_details
        self.args = args
        self.condor_submission = condor_submission

#=================================================================#
