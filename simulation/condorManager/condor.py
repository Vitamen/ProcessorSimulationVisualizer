import commands
import logging
import subprocess
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
        output = commands.getoutput('condor')
        if "Usage:" not in output:
            logging.error(" Condor is not installed on current machine. "
            + "Please install for the condor manager to work correctly")
    
    #=================================================================#
    
    '''
        Submit job to condor using the file specified by the path
        @param The location of the submission file to send to condor
        @return True if the submission is successful. False otherwise
    '''
    def submit(self,path):
        command = "condor_submit"
        exitCode = subprocess.call([command,path])
        if exitCode == 0:
            return True;
        else:
            logging.error("Unable to submit the file " + path + 
                          " to condor. Check path and condor settings")
            return False;
        
        
        
    #=================================================================#
    
    
        
            
            