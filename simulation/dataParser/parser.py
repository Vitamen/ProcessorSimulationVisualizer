import json
import os.path
import subprocess

sampleDataPath = 'dataParser/SampleData/'
outputDataPath = 'static_media/data/'

def readFile(self):
    print(os.path.relpath('sim.out'))
    f = open('sim.out')
    lines = f.readlines()
    f.close()
    print lines
        
def getExperimentList(self):
    print [f for f in os.listdir(sampleDataPath)]
    

## This method will provide a list of all metrics that are available      
def getMetrics():
    metriclist = []
    for line in open('dataParser/metricNameData.txt','r').readlines():
        metriclist.append(line)
        print line
    return metriclist
   
   
def extract(exp,aMetric):
   
    FILE = open(outputDataPath + exp + aMetric + ".txt","w")
    p = subprocess.Popen('cd '+ sampleDataPath + ' ;' + 'grep -ris '+ aMetric + ' .', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line
        #Create an output file
        FILE.write(line)

    FILE.close()
    
        
def getDataFor(self):
    exp = '100M_stream_newsys_effra_fp/' 
    os.path.join(sampleDataPath,exp)
    ## Give shell command to move to correct path
    
    ## Look for Exp folder
    if not os.path.exists(outputDataPath + exp):
        os.makedirs(outputDataPath + exp)
    
    #allMetrics = getMetrics()
    #for aMetric in allMetrics:
    #    print aMetric
    aMetric = "version"
    extract(exp,aMetric)  
        
        

    