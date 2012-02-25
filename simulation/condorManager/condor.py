import logging
import subprocess
import ntpath
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
        retVal = Manager.__callCondor(self, "condor", "-version")
        if retVal == False:
            logging.error("Condor is not installed on curren computer." +
                          " Please visit http://research.cs.wisc.edu/condor/")
    
    
    #=================================================================#
    
    '''
        Submit job to condor using the file specified by the ABSOLUTE path
        
        @param The location of the submission file to send to condor
        @return True if the submission is successful. False otherwise
    '''
    def startJob(self,path):
        retVal = Manager.__callCondor(self, "condor_submit", path)
        if retVal == True :
            self.isRunnng = True 
        return retVal
         
    #=================================================================#
    
    '''
        Stop the condor job with the provided id
        
        @param The id for the job to stkop
        @return True if cancellation is successful. False otherwise
    '''
    def stopJob(self,condorid):
        return Manager.__callCondor(self, "condor_rm", condorid)
        
    #=================================================================#
    
    '''
        Stop all jobs owned by the user
        
        @param The name of the user to stop all jobs
        @return True if cancellation is successful. False otherwise
    '''
    def stopJobAll(self,user):
        return Manager.__callCondor(self, "condor_rm", user)
        
    
    #=================================================================#
    
    '''
        Helper method for calling condor commands and getting results back
        @param The command to call condor
        @param The input to command line
        @return True if call return exit code 0. False otherwise
    '''
    @staticmethod
    def __callCondor(self, command, inputVal):
        try:
            
            #Change to where file is if inputval is a file
            #This is to mimic user's command line behavior
            if ntpath.isfile(inputVal):
                path = ntpath.split(inputVal)
                subprocess.check_output([command,inputVal], cwd=path[0])
            else:
                subprocess.check_output([command,inputVal])
            return True;
        except subprocess.CalledProcessError, e:
            logging.error(str(e))
            return False
    
    #=================================================================#
            