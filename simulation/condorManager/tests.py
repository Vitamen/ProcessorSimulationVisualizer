"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import CondorManager

class SimpleTest(TestCase):
    
    def setUp(self):
        """
        Tests that condor exists on the machine
        """
        self.assert_(CondorManager.Manager())
        self.x = CondorManager.Manager()
       
    
    def testcallCondor(self):
        self.assertTrue(self.x.callCondor(self,["condor_submit", "-verbose", "/home/songdet/Documents/condor.sub"],
                                          filePath="/home/songdet/Documents/"))
        self.assertTrue(self.x.callCondor(self, ["condor_rm", "-all"]))
    