"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import condor

class SimpleTest(TestCase):
    def test_condor(self):
        """
        Tests that condor exists on the machine
        """
        self.assert_(condor.Manager())
        
        """
        Test starting and stopping jobs
        """
        x= condor.Manager()
        self.assertTrue(x.startJob("/home/songdet/Documents/condor.sub"))
        self.assertTrue(x.stopJob("26.0"))