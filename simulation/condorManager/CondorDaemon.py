import sys, time
from Daemon import Daemon

'''
A daemon that monitors condor log file in the background
and notify observer when the log gets updated

@author: songdet
'''
class CondorDaemon(Daemon):
    
    def run(self):
        while True:
            print 'hi!'
            