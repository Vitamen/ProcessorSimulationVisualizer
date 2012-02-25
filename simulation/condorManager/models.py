from django.db import models

'''
    Represents one condor submission (including many condor experiments)
'''
class CondorSubmission(models.Model):
    path = models.CharField(max_length=200, primary_key=True)

#=================================================================#

'''
    Represents one condor experiment running on condor
'''
class CondorJob(models.Model):
    STATUS = (
        (u'U', u'Unexpanded'),
        (u'I', u'Idle'),
        (u'R', u'Running'),
        (u'X', u'Removed'),
        (u'C', u'Completed'),
        (u'H', u'Held'),
        (u'E', u'Submission_err')
        
    )
    
    job_id = models.DecimalField(decimal_places=5, max_digits=15)
    owner = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=STATUS)
    size = models.DecimalField(decimal_places=5, max_digits=15)
    cmd = models.CharField(max_length=200)
    condor_submission = models.ForeignKey(CondorSubmission)

#=================================================================#
    