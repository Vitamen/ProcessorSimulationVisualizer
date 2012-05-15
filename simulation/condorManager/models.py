from django.db import models

'''
Created on Feb 29, 2012

The classes in this file represents a condor submission or a 
condor job submitted to Condor. It will store the relevant information
for each condor submission.
@author: songdet
'''

#=================================================================#

'''
This class represents a single condor job running by Condor
'''
class CondorJob(models.Model):
        job_id = models.CharField(max_length=200, primary_key=True)
        submitted = models.CharField(max_length=200)
        run_time = models.CharField(max_length=200)
        st = models.CharField(max_length=20)
        pri = models.CharField(max_length=20)
        size = models.CharField(max_length=20)
        cmd = models.CharField(max_length=200)

#=================================================================#