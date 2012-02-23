import condor
'''
Created on Feb 22, 2012

@author: songdet
'''
x = condor.Manager()
result = x.submit("/home/songdet/Documents/condor.sub")
print result