import time, logging, ntpath,re, threading
from simulation.settings import CONDOR_DAEMON

'''
A daemon that monitors condor log file in the background
and notify observer when the log gets updated. (Uses listener
pattern.) The listener must have method notify() implemented

Preconditions:
1) The log file that is given exists and is being updated in real-time
by the Condor cluster
2) The condorSubmission model contains the relevant condor jobs for
the specific condor submission being monitored

@author: Songdet
'''
class CondorDaemon(threading.Thread):
    
    '''
        Check if logFile exists and can be opened and check if callback
        is callable. If either of this is not satisfied, error is raised
        
        @param The name of the log file that the daemon should track
        @param The condorSubmission model representing the current submission
    '''
    def __init__(self,logFile, condorSubmission):
        
        #Used to store the collection of observers to notify when
        #log file changes
        self.observerCollection = []
        
        #Check if logFile is valid. If not, raise error. Otherwise open
        absname = ntpath.abspath(logFile)
        try: 
            ntpath.exists(absname)
        except EnvironmentError:
            logging.error("The logFile to watch is not a valid file")
            raise
        self.logFile = open(logFile, "r")
        
        #Store condorSubmission jobs for later updates
        self.condorSubmission = condorSubmission
        self.condorJobs = condorSubmission.condorJobs
        
        #Set Thread as daemon and all super constructor
        super(CondorDaemon,self).__init__()
        self.running = True
        
    #=================================================================#
    
    '''
        Stop the current thread. Thread completes work and close down
    '''
    def stop(self):
        self.running = False

    #=================================================================#
    
    '''
        Check the logFile for update every interval seconds. If
        update is detected, notify all registered observers
        
        ** This method is called by start in Thread. Do not call this
        method directly. call start() instead
    '''
    def run(self):
        #Time to update interval & time to wait if the log is currently
        #being updated by condor
        interval = CONDOR_DAEMON['interval']
        waitTime = 2
        
        #Loop the daemon, checking update every interval time
        #If new changes are found, call observer with the changes
        while self.running:
            location = self.logFile.tell()
            lines = self.logFile.readlines()
            if lines:
                #If the last line is not ..., the log is being read in
                #Reset and wait a few second before trying again
                if lines[len(lines)-1] != '...':
                    self.logFile.seek(location)
                    time.sleep(waitTime)
                    continue
                else :
                    retVal = self.__getUpdates(lines)
                    self.__notifyObservers(retVal)
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
        self.observerCollection.append(observer)
        return True
    
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
        Parse the array of lines and return an array of information about
        the updates. Update the condor submission accordingly
        @param The array of lines that's new in this submission
        @return The array of changes made
    '''
    def __getUpdates(self, lines):
        curVal = ''
        retVal = {}
        
        #Scan through the array until ... is found
        #When ... is found, we found a full message.
        #Do necessary processing and updates
        for line in lines:
            if line.find('...') != -1:
                condorJob = self.__processUpdates(curVal)
                condorJobDict = {condorJob.job_id : condorJob}
                retVal.update(condorJobDict)
                curVal = ''
            else:
                curVal = curVal + "\n" + line
        return retVal
    
    #=================================================================#
    
    '''
        Process the updates contained in curVal, update database, and
        return the information
    '''
    def __processUpdates(self,curVal):
        
        #Determine status
        curVal = curVal.strip()
        status = curVal[0:3]
        statusDetails = curVal[curVal.find(")")+1:len(curVal)]
        statusDetails = statusDetails.strip()
        
        #Get the process model from list of condor jobs
        procId = curVal[curVal.find("(")+1:curVal.find(")")-4]
        procId = re.sub('^[0]+', '', procId)
        procId = re.sub('[.][0]+','.',procId)
        if procId[len(procId)-1] == '.': procId = procId + "0"
        for curJob in self.condorJobs:
            if curJob.job_id == procId:
                condorJob = curJob
                break
        
        #Determine status and update the job and add to retVal accordingly
        try:
            condorJob.status = status
            condorJob.status_details = statusDetails
        except UnboundLocalError:
            logging.error("Process id doesn't match")
            raise
        return condorJob
        
    #=================================================================#

    '''
        Notify all registered observers that new lines have been added
    '''
    def __notifyObservers(self,condorJobs):
        for observer in self.observerCollection:
            observer.notify(condorJobs)
            
    #=================================================================#
        