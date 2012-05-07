import json
import os.path
import subprocess
from experimentManager.models import *

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

def parseExperiment (exp):
    exp = "100M_stream_effra"
    benchmarkSuite, created = BenchmarkSuite.objects.get_or_create(suite="suite")
    experiment_object = findOrCreateExperimentByName(exp)
    path = os.path.join(sampleDataPath,exp)
    ## Look for Exp folder
    #if not os.path.exists(outputDataPath + exp):
    #    os.makedirs(outputDataPath + exp)
    
    ## Look for all the benchmarks
    benchmarksProcess = subprocess.Popen("cd "+ path+"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    oneBenchmark = "";
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarktoken = tokens[0].rstrip("\n")
        benchmark_object = findOrCreateBenchmarkByName(benchmarktoken)
        matchingBenchmarks = ExperimentBenchmark.objects.filter(expname=exp, bmname=benchmarktoken)
        oneBenchmark = benchmarktoken
        if len(matchingBenchmarks) == 0:
            experimentBenchmark_object = ExperimentBenchmark(expname=experiment_object, bmname=benchmark_object)
            experimentBenchmark_object.save()
    
    path = os.path.join(sampleDataPath,exp,oneBenchmark)
    metricsProcess = subprocess.Popen("cd "+path+"; grep '' *", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in metricsProcess.stdout.readlines():
        tokens = line.split("\"")
        if len(tokens) > 1:
            metricToken = tokens[1]
            metric_object = findOrCreateMetricByName(metricToken)
            matchingMetrics = ExperimentMetric.objects.filter(expname=exp, metricname=metricToken)
            if len(matchingMetrics) == 0:
                experimentMetric_object = ExperimentMetric(expname=experiment_object, metricname=metric_object)
                experimentMetric_object.save()
    print ExperimentMetric.objects.count()

   
def extractBenchmarksFromExperiments (exp):
    exp = "100M_np_base"
    benchmarkSuite, created = BenchmarkSuite.objects.get_or_create(suite="suite")
    experiment_object = findOrCreateExperimentByName(exp)
    path = os.path.join(sampleDataPath,exp)
    print path
    ## Look for Exp folder
    #if not os.path.exists(outputDataPath + exp):
    #    os.makedirs(outputDataPath + exp)
    
    ## Look for all the benchmarks
    print path
    benchmarksProcess = subprocess.Popen("cd "+ path+"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarktoken = tokens[0].rstrip("\n")
        print "[" + benchmarktoken + "]"
        benchmark_object = findOrCreateBenchmarkByName(benchmarktoken)
        matchingBenchmarks = ExperimentBenchmark.objects.filter(expname=exp, bmname=benchmarktoken)
        if len(matchingBenchmarks) == 0:
            experimentBenchmark_object = ExperimentBenchmark(expname=experiment_object, bmname=benchmark_object)
            experimentBenchmark_object.save()
    print ExperimentBenchmark.objects.count()

def extractMetricFromExperiment (exp,aMetric):

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
    FILE.write("datatest[\""+exp+"\"] = [" )
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
        extractMetricFromExperiment(exp,aMetric.rstrip('\n'))  
