import json
import os.path
import subprocess
from simulation.settings import EXP_ROOT_DIR, PROJECT_PATH, PARSE_ROOT_DIR
from simulation.experimentManager.models import *

sampleDataPath = os.path.join(PROJECT_PATH, 'dataParser', 'SampleData')
outputDataPath = PARSE_ROOT_DIR

#######################################################

def readFile(self):
    f = open('sim.out')
    lines = f.readlines()
    f.close()

#######################################################

def getExperimentList(self):
    print [f for f in os.listdir(sampleDataPath)]

#######################################################

def parseExperiment (subName, curExpName, metricType):
    #Get current experiment object from databases
    experiment_object = Experiments.objects.get(submissionName=subName, expName=curExpName)
    experiment_pk = experiment_object.pk
    path = os.path.join(EXP_ROOT_DIR,subName,"data",curExpName)

    #Look for all the benchmarks
    benchmarksProcess = subprocess.Popen("cd "+ path+"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    benchFound = False
    for line in benchmarksProcess.stdout.readlines():
        #Extract Benchmark names
        tokens = line.split(" ")
        benchmarktoken = tokens[0].rstrip("\n")
        benchPath = os.path.join(path,benchmarktoken)
    
        #Go through each possible benchmark file to get metric out
        #Once a file with metric is found, extract and exit
        metricsProcess = subprocess.Popen("cd "+benchPath+"; grep '' *", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in metricsProcess.stdout.readlines():
            tokens = line.split("\"")
            if len(tokens) > 1:
                benchFound = True
                metricToken = tokens[1]
                metric_object = findOrCreateMetricByName(metricToken)
                matchingMetrics = ExperimentMetric.objects.filter(expname=experiment_pk, metricname=metricToken)
                if len(matchingMetrics) == 0:
                    experimentMetric_object = ExperimentMetric(expname=experiment_object, metricname=metric_object)
                    experimentMetric_object.save()
        if benchFound: break


#######################################################

def extractMetricFromExperiment (subName, expName,aMetric):      
    metric = findOrCreateMetricByName(aMetric)
    if metric.metrictype == 'HISTOGRAM':
        extractHistogramMetricFromExperiment(subName,expName,aMetric)
    elif metric.metrictype == 'SCATTERPLOT':
        extractScatterplotMetricFromExperiment(subName,expName,aMetric)

#######################################################

def extractHistogramMetricFromExperiment (subName,expName,aMetric):
    ##Create an output file with the metric name.
    fileName = generateOutputPathForExperimentAndHistogramMetric(subName, expName, aMetric)
    FILE = open(fileName,"w")
    
    ##Grep for the given metric 
    path = os.path.join(EXP_ROOT_DIR,subName,"data",expName) 
    grepRes = subprocess.Popen('cd '+ path + ' ;' + 'grep -ris \\"'+ aMetric + '\\" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   
    ## Open json object
    FILE.write("datatest[\""+expName +"\"] = [" )
    
    ##Parse and write data
    for line in grepRes.stdout.readlines():
        ##Now parse the line to extract the benchmark and value

        tokens = line.split("/")
        print tokens
        simple = tokens[1].rstrip(",\n")
        simple = simple.lstrip("sim.out:")
        simple = simple.lstrip('"' + aMetric + '"' + ":")
        simple = simple.lstrip(' ')
        print simple
        if not simple.find("[") == 0:
            simple= "[" + simple + "]"
        #Create an output file
        FILE.write("{\"" + tokens[0] + "\":" + simple + "},")

    FILE.write("]")
    FILE.close()

#######################################################

def extractScatterplotMetricFromExperiment(subName, expName, aMetric):

    #Go to base folder and get out benchmark names
    basePath = os.path.join(EXP_ROOT_DIR,subName,"data",expName) 
    benchmarksProcess = subprocess.Popen("cd "+basePath+"; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);  
      
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarkname= tokens[0].rstrip("\n")
    
        ##Grep for the given metric 
        grepRes = subprocess.Popen('cd '+ basePath+"/"+benchmarkname + '; grep -ris "'+ aMetric + '" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       
        ## Look for Exp folder
        folderName = generateOutputFolderForExperimentAndScatterPlotMetricAndBenchmark(subName, expName, aMetric, benchmarkname)

        ##Create an output file with the metric name.
        FILE = open(folderName + "/" + aMetric + ".js","w")
       
        ## Open json object
        FILE.write("datatest[\"" + expName + benchmarkname + "\"] =" )
        
        ##Parse and write data
        for dataline in grepRes.stdout.readlines():
            dataArray = dataline[dataline.index('['):dataline.index(']')+1];
            FILE.write(dataArray)
    FILE.write(";")
    FILE.close()

#######################################################

def extractBenchmarksFromExperiments (subName,curExpName):
    myPath = os.path.join(EXP_ROOT_DIR,subName,"data",curExpName)
    retBenchMarks = []
    benchmarksProcess = subprocess.Popen("cd "+ myPath+"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarktoken = tokens[0].rstrip("\n")
        benchmark_object = findOrCreateBenchmarkByName(benchmarktoken)
        retBenchMarks.append(benchmark_object)
    return retBenchMarks

#######################################################

def generateOutputFolderForExperimentAndHistogramMetric(subName, expName):
    folderName = os.path.join(outputDataPath,subName, expName)
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    return folderName

#######################################################

def generateOutputPathForExperimentAndHistogramMetric(subName, expName, metric):
    resultFolder = generateOutputFolderForExperimentAndHistogramMetric(subName, expName);
    resultFile = os.path.join(resultFolder, metric)
    resultFile = resultFile + ".js"
    return resultFile

#######################################################

def generateBaseOutputFolderForExperimentAndScatterPlotMetric(subName,expName):
    folderName = os.path.join(outputDataPath,subName,expName)
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    return folderName;

#######################################################

def generateOutputFolderForExperimentAndScatterPlotMetricAndBenchmark(subName,expName, metric, benchmark):
    baseFolderName = generateBaseOutputFolderForExperimentAndScatterPlotMetric(subName, expName);
    folderName = os.path.join(baseFolderName, benchmark)
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    return folderName       
#######################################################

