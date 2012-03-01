'''
Created on Feb 29, 2012

@author: songdet
'''

class CondorSubmission:
    
    def __init__(self, path, condorJobs=None):
        self.path =path
        self.condorJobs = condorJobs

#=================================================================#

class CondorJob:
    
    def __init__(self, job_id, owner, status, status_details, size,
                 cmd, condor_submission):
        self.job_id = job_id
        self.owner = owner
        self.status = status
        self.status_details = status_details
        self.size = size
        self.cmd =cmd
        self.condor_submission = condor_submission

#=================================================================#
