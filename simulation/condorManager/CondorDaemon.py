import time, hashlib, logging, os, ntpath
from Daemon import Daemon

'''
A daemon that monitors condor log file in the background
and notify observer when the log gets updated. (Uses listener
pattern. The listener must have method notify() implemented

@author: Songdet
'''
class CondorDaemon(Daemon):
    
    '''
        Check if logFile exists and can be opened and check if callback
        is callable. If either of this is not satisfied, error is raised
        
        @param The name of the log file that the daemon should track
    '''
    def __init__(self,logFile, condorSubmission):
        
        #Used to store the collection of observers to notify when
        #log file changes
        self.observerCollection = []
        
        #Check if logFile is valid. If not, raise error. Otherwise open
        absname = ntpath.abspath(logFile)
        try: 
            os.stat(absname)
        except EnvironmentError:
            logging.error("The logFile to watch is not a valid file")
            raise
        self.logFile = open(absname, "r")

    #=================================================================#
    
    def __del(self):
        self.close()
        
    #=================================================================#
    
    '''
        Check the logFile for update every interval seconds. If
        update is detected, notify all registered observers
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
                self.__notifyObservers(lines)
            else:
                self.logFile.seek(location)              
            time.sleep(interval)
    
    #=================================================================#
    
    '''
        Register the observer to callback to when log file gets updated
        @param The observer object to listen to file changes.
        @return True if registered successfully. False otherwise
    '''
    def registerObserver(self, observer):
        if hasattr(observer, 'notify'):
            self.observerCollection.append(observer)
            return True
        else:
            return False
    
    #=================================================================#  
    
    '''
        Remove the observer previously registered to the daemon
        @param The observer object to remove
        @return True if removed successfully, false otherwise
    '''
    def unregisterObserver(self, observer):
        try:
            self.observerCollection.remove(observer)
            return True
        except ValueError:
            return False
        
    #=================================================================#
        
    '''
        Notify all registered observers that new lines have been added
    '''
    def __notifyObservers(self,lines):
        for observer in self.observerCollection:
            observer.notify(lines)
            
    #=================================================================#
        