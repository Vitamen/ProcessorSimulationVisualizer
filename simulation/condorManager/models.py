from django.db import models

'''
    Represents one condor submission (including many condor experiments)
'''
class CondorSubmission(models.Model):
    path = models.CharField(max_length=200, primary_key=True)
    
    def __unicide__(self):
        return self.path

#=================================================================#

'''
    Represents one condor experiment running on condor
'''
class CondorJob(models.Model):
    
    CONDOR_LOG_STATUS = (
                    (u'000' , u'Submit') ,
                    (u'001' , u'Execute') ,
                    (u'002' , u'Executable_error') ,
                    (u'003' , u'Checkpointed') ,
                    (u'004' , u'Job_evicted') ,
                    (u'005' , u'Job_terminated') ,
                    (u'006' , u'Image_size') ,
                    (u'007' , u'Shadow_exception') ,
                    (u'008' , u'Generic') ,
                    (u'009' , u'Job_aborted') ,
                    (u'010' , u'Job_suspended') ,
                    (u'011' , u'Job_unsuspended') ,
                    (u'012' , u'Job_held') ,
                    (u'013' , u'Job_released') ,
                    (u'014' , u'Node_execute') ,
                    (u'015' , u'Node_terminated') ,
                    (u'016' , u'Post_script_terminated') ,
                    (u'017' , u'Globus_submit') ,
                    (u'018' , u'Globus_submit_failed') ,
                    (u'019' , u'Globus_resource_up') ,
                    (u'020' , u'Globus_resource_down') ,
                    (u'021' , u'Remote_error')
                    )
    
    job_id = models.CharField(max_length=30, primary_key=True)
    owner = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=CONDOR_LOG_STATUS)
    size = models.DecimalField(decimal_places=5, max_digits=15)
    cmd = models.CharField(max_length=200)
    condor_submission = models.ForeignKey(CondorSubmission)
    
    def __unicode__(self):
        return self.job_id

#=================================================================#
    