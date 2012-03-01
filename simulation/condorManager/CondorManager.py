import logging, subprocess, os ,ntpath, re, CondorDaemon
from models import CondorSubmission, CondorJob

'''
Provides the interface for talking to Condor cluster.

Preconditions: 
1) A condor.sub file must have been generated and accessible 
by this module through I/O call
2) The OS the server is running on must have condor installed

Postconditions:
Condor Manager is instantiated and ready to communicate with condor
cluster

Created on Feb 22, 2012

@author: songdet
'''
class Manager:
    
    '''
        Constructor checks if condor is installed. If it's not installed, 
        report to error logger
    '''
    def __init__(self):
        self.daemonMap = {}
        retVal = Manager.callCondor(self, ["condor", "-version"])
        if retVal == False:
            logging.error("Condor is not installed on current computer." +
                          " Please visit http://research.cs.wisc.edu/condor/")
    
    
    #=================================================================#
    
    '''
        Submit job to condor using the file specified by the ABSOLUTE path
        
        @param The location of the submission file to send to condor.
               The submission file must specify a log location
        @return The CondorDaemon started by the process. False otherwise
    '''
    def startJob(self,path):
        
        #Check that the file specified by path exists.
        absname = ntpath.abspath(path)
        try :
            ntpath.exists(absname)
        except : 
            logging.error("The path specified does not exist")
            raise
        
        #Extract log file name for CondorDaemon
        condorSub = open(path, "r").read()
        lineFound = re.search("^[Ll]og[ \t]*=.+", condorSub, re.MULTILINE)
        if lineFound :
            logFile = re.split("=[ \t]*", lineFound.group(0))[1]
        if not logFile :
            logging.error("The submission file did not specify a log location")
            raise
        
        #Submit to condor & return if false
        retVal = Manager.callCondor(self, ["condor_submit", "-verbose", path])
        if retVal == False:
            return False
        
        #Create a model of condor submission along with condor jobs
        condorSubmission = self.getModels(path, retVal)
        
        #Spawn CondorDaemon process to keep track of condor submission
        #Store this in a map. If the map already contain this, stop previous
        #job and run again
        try:
            m = self.daemonMap[path]
            m.stop()
        except KeyError:
            pass
        m = CondorDaemon.CondorDaemon(logFile,condorSubmission).start()
        self.daemonMap[path] = m
        return m
         
    #=================================================================#
    
    '''
        Stop the condor job with the provided id
        
        @param The id for the job to stkop
        @return True if cancellation is successful. False otherwise
    '''
    def stopJob(self,condorid):
        return Manager.callCondor(self, "condor_rm", condorid)
        
    #=================================================================#
    
    '''
        Stop all jobs owned by the user
        
        @param The name of the user to stop all jobs
        @return True if cancellation is successful. False otherwise
    '''
    def stopJobAll(self,user):
        return Manager.callCondor(self, "condor_rm", user)
        
    
    #=================================================================#

    '''
        Helper method for calling condor commands and getting results back
        @param The command and arguments to call condor with
        @param Change to filePath and execute command from there if not false
        @return Output value if ran successfully, false otherwise
    '''
    @staticmethod
    def callCondor(self, command, filePath=False):
        try:
            
            #Change to where file is if filePath is given
            #This is to mimic user's command line behavior
            if filePath:
                path = ntpath.split(filePath)
                output = subprocess.check_output(command, cwd=path[0])
            else:
                output = subprocess.check_output(command)
            return output
        except subprocess.CalledProcessError, e:
            logging.error(str(e))
            return False
    
    #=================================================================#
    
    '''
        Helper method that uses retVal to create and store condor submissions
        and condor jobs
        @param the path to start this job
        @param the value use to create model
        @return the CondorSubmission model that contains information about condor
                jobs
    '''
    def getModels(self,path,retVal):
        
        #Split jobs
        jobs = re.split("** Proc ", retVal)
        
        #Create a condor submission
        #for job in jobs:
            #Create the model for a condor job
            
            #Set the variables based on extracts from job
            
            #Add the condor job to condor submission
        
            