"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import CondorDaemon
from CondorData import *
import time, jsonpickle
from simulation.settings import CONDOR_DAEMON

class TestCondorDaemon(TestCase):
    
    '''
        Set up things to test condor with
    '''
    def setUp(self):
        #Set up the file to test
        self.path = "./tmp2"
        
        #Set up the model
        self.con = CondorSubmission(path='condor.sub')
        self.p1 = CondorJob(job_id="110.0", 
                       owner="songdet", 
                       status="Submit", 
                       status_details="xx",
                       size=20, 
                       cmd='hi.txt',
                        condor_submission=self.con)
        self.p2 = CondorJob(job_id="111.0", 
                       owner="songdet", 
                       status="Submit", 
                       status_details="xx",
                       size=20, 
                       cmd='hi.txt',
                        condor_submission=self.con)
        self.con.condorJobs = [self.p1,self.p2]
        
        #Generate
        self.x = CondorDaemon.CondorDaemon(self.path,self.con)

        #Tests
        self.x.start()

    #=================================================================#
    
    '''
        Simple tests to check if register & unregister
        observers work correctly
    '''
    def testRegisterUnregisterObserver(self):
        self.assertFalse(self.x.registerObserver('2'))
        self.assertFalse(self.x.unregisterObserver('2'))
        
        x = ListenerClass()
        self.assertTrue(self.x.registerObserver(x))
        self.assertTrue(self.x.unregisterObserver(x))
        self.assertFalse(self.x.unregisterObserver(x))
    
    #=================================================================#
    
    '''
        Simple tests to check if run works correctly
    '''
    ''' def testRunCondorDaemon(self):
        myX = ListenerClass()
        self.x.registerObserver(myX)
        print(len(self.x.observerCollection))
        time.sleep(CONDOR_DAEMON['interval'] + 3)
        f = open(self.path,'a')
        f.write("\n011 (111.000.000) 02/17 12:03:10 Job was unsuspended.\n...")
        f.flush()
        print(self.x.is_alive())
        time.sleep(CONDOR_DAEMON['interval'] + 3)
        self.x.stop()
        time.sleep(CONDOR_DAEMON['interval'] + 3)
        print(self.x.is_alive())
    '''
    
#=================================================================#
#=================================================================#        

class TestCondorManager(TestCase):
     def setUp(self):
         return
     
#=================================================================#
#=================================================================#

class ListenerClass:
    def notify(self, msg):
        writerr = open("./test.tmp",'a')
        for val in msg:
            stringVal = str(jsonpickle.encode(msg[val], max_depth=1))
            writerr.write(stringVal+"\n")
        writerr.flush()

#=================================================================#
#=================================================================#
