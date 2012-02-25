import time, hashlib, logging, os, ntpath
from Daemon import Daemon

'''
A daemon that monitors condor log file in the background
and notify observer when the log gets updated

@author: Songdet
'''
class CondorDaemon(Daemon):
    
    '''
        Check if logFile exists and can be opened and check if callback
        is callable. If either of this is not satisfied, error is raised
        
        @param The name of the log file that the daemon should track
        @param The callback function that the daemon should call with
               new lines when changes happen
    '''
    def __init__(self,logFile, callback):

        #Check if logFile is valid. If not, raise error. Otherwise open
        absname = ntpath.abspath(logFile)
        try: 
            os.stat(absname)
        except EnvironmentError:
            logging.error("The logFile to watch is not a valid file")
            raise
        self.logFile = open(absname, "r")
        
        #Check if callback is callable
        if not hasattr(callback, '__call__'):
            logging.error("The callback function you call with is not callable")
            raise
        else:
            self.callback = callback

    #=================================================================#
    
    def __del(self):
        self.close()
        
    #=================================================================#
    
    '''
        Check the logFile for update every interval seconds. If
        update is detected, send the newlines to callback function
    '''
    def run(self):
        #Interval to run updates
        interval = 10
        
        #Loop the daemon, checking update every interval time
        #If new changes are found, call observer
        while True:
            location = self.logFile.tell()
            lines = self.logFile.readlines()
            if lines:
                self.callback(lines)
            else:
                self.logFile.seek(location)              
            time.sleep(interval)
    
    #=================================================================#
        