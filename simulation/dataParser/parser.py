import json
import os.path
import subprocess
from simulation.settings import  PROJECT_PATH, PARSE_ROOT_DIR
from simulation.experimentManager.models import *
import re
from django.core.exceptions import ObjectDoesNotExist

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

def parseExperiment (subName, curExpName):
    #Get current experiment object from databases
    experiment_object = Experiments.objects.get(submissionName=subName, expName=curExpName)


def parseExperimentWithRootDirectory (rootDirectory):
    experimentName = getExperimentNameFromRootDirectory(rootDirectory)
    submissionName = getSubmissionNameFromRootDirectory(rootDirectory)
    experiment_object, created = Experiments.objects.get_or_create(expName = experimentName, submissionName = submissionName, rootDirectory = rootDirectory)
    
    path = rootDirectory;
    #Look for all the benchmarks
    benchmarksProcess = subprocess.Popen("cd \""+ path+"\"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    benchFound = False
    for line in benchmarksProcess.stdout.readlines():
        #Extract Benchmark names
        tokens = line.split(" ")
        for benchmarktoken in tokens:
            benchmarktoken = tokens[0].rstrip("\n")
            benchPath = os.path.join(path,benchmarktoken)
            benchmark, created = Benchmarks.objects.get_or_create(name = benchmarktoken)
            experimentBenchmark, created = ExperimentBenchmark.objects.get_or_create(expName=experiment_object, benchmark = benchmark)
        
            #Go through each possible benchmark file to get metric out
            #Once a file with metric is found, extract and exit
            metricsProcess = subprocess.Popen("cd \""+benchPath+"\"; grep '' *", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in metricsProcess.stdout.readlines():
                tokens = line.split("\"")
                if len(tokens) > 1:
                    benchFound = True
                    metricToken = tokens[1]
                    metric_object = findOrCreateMetricByName(metricToken)
                    matchingMetrics = ExperimentMetric.objects.filter(expname=experiment_object, metricname=metricToken)
                    
                    if len(matchingMetrics) == 0:
                        experimentMetric_object = ExperimentMetric(expname=experiment_object, metricname=metric_object)
                        experimentMetric_object.save()
            if benchFound: break
#######################################################

def extractMetricFromExperiment (subName, expName, aMetric):      
    metric, created = Metric.objects.get_or_create(metricname = aMetric)
    if metric.isAggregate:
        extractMetricFromExperimentAndEvalStatement(subName,expName,aMetric)
    else:
        if metric.metrictype == 'HISTOGRAM':
            extractHistogramMetricFromExperiment(subName,expName,aMetric)
        elif metric.metrictype == 'SCATTERPLOT':
            extractScatterplotMetricFromExperiment(subName,expName,aMetric)

#######################################################

def extractMetricFromExperimentAndEvalStatement(subName, expName, evalMetricName):
    experiment = Experiments.objects.get(expName = expName)
    metric = Metric.objects.get(metricname = evalMetricName)
    metricAggregate = MetricAggregate.objects.get(metric = metric)
    evalString = metricAggregate.evalString
    pattern = r'{\w+}'
    regex = re.compile(pattern, re.IGNORECASE)
    allMetricData = []
    allMetricNames = []
    isHistogram = metric.metrictype == 'HISTOGRAM'
    for match in regex.finditer(evalString):
        metricName =  match.group();
        metricName = metricName[1:-1]
        if isHistogram:
            metricData = getHistogramDataForMetricFromExperiment(subName, experiment, metricName)
        else:
            metricData = getScatterplotDataForMetricFromExperiment(subName, experiment, metricName)
        allMetricData.append(metricData)
        allMetricNames.append(metricName)
    
    aggregateData = []
    numDataPoints = 0;
    if len(allMetricData) == 0:
        return
    else:
        numDataPoints = len(allMetricData[0])

    aggregateBenchmarks = []
    for i in range(0, numDataPoints):
        curEvalString = evalString.strip();
        for match in regex.finditer(evalString):
            lastindex = 0
            if not match.lastindex == None:
                lastindex = match.lastindex
            dataKeyPair = allMetricData[lastindex][i]
            for key in dataKeyPair:
                curEvalString = curEvalString.replace(match.group(), str(dataKeyPair[key][0]))
        aggregateBenchmarks.append(key)  
        aggregateData.append(eval(curEvalString))

    fileName = generateOutputPathForExperimentAndHistogramMetric(subName, expName, evalMetricName)
    FILE = open(fileName,"w")
    print fileName

    ## Open json object
    FILE.write("datatest[\""+expName +"\"] = [" )
    
    ##Parse and write data
    i = 0;
    print aggregateBenchmarks
    for dataPoint in aggregateData:
        print dataPoint
        dataPointString = str(dataPoint)
        if not dataPointString.find("[") == 0:
            dataPointString= "[" + dataPointString + "]"
        #Create an output file
        FILE.write("{\"" + aggregateBenchmarks[i]+"\":" + dataPointString + "},")
        i = i + 1

    FILE.write("]")
    FILE.close()
        
def getHistogramDataForMetricFromExperiment(subName, experiment, metric):
    fileName = generateOutputPathForExperimentAndHistogramMetric(subName, experiment.expName, metric)
    if not os.path.exists(fileName):
        extractHistogramMetricFromExperiment(subName, experiment.expName, metric)
    
    FILE = open(fileName, "r")
    fileContents = FILE.read();
    pattern = r'\[\{.+,\]'
    regex = re.compile(pattern, re.IGNORECASE)
    matches = regex.finditer(fileContents)
    jsondata = [];
    for match in matches:
        jsonstring = match.group();
        jsonstring = jsonstring.replace(",]","]")
        jsondata = json.loads(jsonstring)
    return jsondata

def getScatterplotDataForMetricFromExperiment(subName, experiment, metric):
    return []
        

def extractHistogramMetricFromExperiment (subName,expName,aMetric):
    ##Create an output file with the metric name.
    fileName = generateOutputPathForExperimentAndHistogramMetric(subName, expName, aMetric)
    FILE = open(fileName,"w")
    
    ##Grep for the given metric 
    experiment = Experiments.objects.get(submissionName = subName, expName = expName)
    path = experiment.rootDirectory
    grepRes = subprocess.Popen('cd \"'+ path + '\" ;' + 'grep -ris \\"'+ aMetric + '\\" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   
    ## Open json object
    FILE.write("datatest[\""+expName +"\"] = [" )
    
    ##Parse and write data
    for line in grepRes.stdout.readlines():
        ##Now parse the line to extract the benchmark and value

        tokens = line.split("/")
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

#######################################################

def extractScatterplotMetricFromExperiment(subName, expName, aMetric):

    experiment = Experiments.objects.get(submissionName = subName, expName = expName)
    #Go to base folder and get out benchmark names
    basePath = experiment.rootDirectory 
    benchmarksProcess = subprocess.Popen("cd \""+basePath+"\"; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);  
      
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarkname= tokens[0].rstrip("\n")
    
        ##Grep for the given metric 
        grepRes = subprocess.Popen('cd \"'+ basePath+"/"+benchmarkname + '\"; grep -ris "'+ aMetric + '" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       
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
    try:
        experiment = Experiments.objects.get(submissionName = subName, expName = curExpName)
    except:
        return []
    
    retBenchMarks = ExperimentBenchmark.objects.filter(expName = experiment)
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

def getExperimentNameFromRootDirectory(rootDirectory):
    tokens = rootDirectory.split("/")
    experimentName = tokens[-1]
    return experimentName

#######################################################

def getSubmissionNameFromRootDirectory(rootDirectory):
    tokens = rootDirectory.split("/")
    submissionName = tokens[-2]
    return submissionName
