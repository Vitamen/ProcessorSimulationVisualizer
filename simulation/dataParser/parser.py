import json
import os.path
import subprocess

sampleDataPath = 'dataParser/SampleData/'
outputDataPath = 'static_media/data/'

def readFile(self):
    f = open('sim.out')
    lines = f.readlines()
    f.close()
        
def getExperimentList(self):
    print [f for f in os.listdir(sampleDataPath)]
    

## This method will provide a list of all metrics that are available      
def getMetrics():
    metriclist = []
    for line in open('dataParser/metricNameData.txt','r').readlines():
        metriclist.append(line)
    return metriclist
   
   
def extract(exp,aMetric):
    path = os.path.join(sampleDataPath,exp)
    ## Give shell command to move to correct path
    
    ## Look for Exp folder
    if not os.path.exists(outputDataPath + exp):
        os.makedirs(outputDataPath + exp)
        
        
    ##Create an output file with the metric name.
    FILE = open(outputDataPath + exp + "/" + aMetric + ".js","w")
    
    ##Grep for the given metric 
    p = subprocess.Popen('cd '+ path + ' ;' + 'grep -ris \\"'+ aMetric + '\\" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   
    ## Open json object
    FILE.write("var data = [")
    ##Parse and write data
    for line in p.stdout.readlines():
        ##Now parse the line to extract the benchmark and value
        tokens = line.split("/")
        #print tokens
        print tokens
        simple = tokens[1].rstrip(",\n")
        simple = simple.lstrip("sim.out:")
        simple = simple.lstrip('"' + aMetric + '"' + ":")
        simple = simple.lstrip(' ')
        if not simple.find("[") == 0:
            simple= "[" + simple + "]"
        #Create an output file
        FILE.write("{\"" + tokens[0] + "\":" + simple + "},")

    FILE.write("]")
    FILE.close()
    
        
def getDataFor(self):
    
    exp = '100M_stream_newsys_effra_fp/' 
    os.path.join(sampleDataPath,exp)
    ## Give shell command to move to correct path
    
    ## Look for Exp folder
    if not os.path.exists(outputDataPath + exp):
        os.makedirs(outputDataPath + exp)
    
    allMetrics = getMetrics()
    for aMetric in allMetrics:
    #    print aMetric
    #aMetric = "version"
        extract(exp,aMetric.rstrip('\n'))  
