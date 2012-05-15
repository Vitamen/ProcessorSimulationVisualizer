import logging, subprocess, ntpath, sys
from simulation.condorManager import CondorJobPopulate
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
class Manager(object):
    
    '''
        Constructor checks if condor is installed. If it's not installed, 
        report to error logger
    '''
    def __init__(self):
        retVal = Manager.callCondor(self, ["condor", "-version"])
        if retVal == False:
            logging.error("Condor is not installed on current computer." +
                          " Please visit http://research.cs.wisc.edu/condor/")
    
    
    #=================================================================#
    
    '''
        Submit job to condor using the file specified by the ABSOLUTE path
    '''
    def startJob(self,path):
        #Check that the file specified by path exists.
        absname = ntpath.abspath(path)
        try :
            ntpath.exists(absname)
        except : 
            logging.error("The path specified does not exist")
            raise
        
        #Submit to condor & return if false
        retVal = Manager.callCondor(self, ["condor_submit", path])
        if retVal == False:
            return False
         
    #=================================================================#
    
    '''
        Stop the condor job with the provided id
        
        @param The id for the job to stkop
        @return True if cancellation is successful. False otherwise
    '''
    def stopJob(self,condorid):
        return Manager.callCondor(self, ["condor_rm", condorid])
        
    #=================================================================#
    
    '''
        Stop all jobs currently running
    '''
    def stopAllJobs(self):
        return Manager.callCondor(self, ["condor_rm", "-all"])
        
    #=================================================================#
    
    '''
        Get the status of local Condor jobs
    '''
    def getStatus(self):
        return Manager.callCondor(self, "condor_q")
    
    #=================================================================#
    
    '''
        Get the status of local Condor jobs in long format
    '''
    def getStatusLong(self, myId):
        return Manager.callCondor(self, ["condor_q", myId, "-long"])
    
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
        except (subprocess.CalledProcessError,OSError), e:
            logging.error(str(e))
            return False
    
    #=================================================================#