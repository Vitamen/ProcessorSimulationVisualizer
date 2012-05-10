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

   
def extractBenchmarksFromExperiments (exp):
    exp = "100M_np_base"
    benchmarkSuite, created = BenchmarkSuite.objects.get_or_create(suite="suite")
    experiment_object = findOrCreateExperimentByName(exp)
    path = os.path.join(sampleDataPath,exp)

    benchmarksProcess = subprocess.Popen("cd "+ path+"; ls;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarktoken = tokens[0].rstrip("\n")
        benchmark_object = findOrCreateBenchmarkByName(benchmarktoken)
        matchingBenchmarks = ExperimentBenchmark.objects.filter(expname=exp, bmname=benchmarktoken)
        if len(matchingBenchmarks) == 0:
            experimentBenchmark_object = ExperimentBenchmark(expname=experiment_object, bmname=benchmark_object)
            experimentBenchmark_object.save()

def extractMetricFromExperiment (exp,aMetric):

    path = os.path.join(sampleDataPath,exp)
    ## Give shell command to move to correct path        
    
    metric = findOrCreateMetricByName(aMetric)
    if metric.metrictype == 'HISTOGRAM':
        extractHistogramMetricFromExperiment(exp, aMetric)
    elif metric.metrictype == 'SCATTERPLOT':
        extractScatterplotMetricFromExperiment(exp, aMetric)

def extractHistogramMetricFromExperiment (exp,aMetric):
    print "EXTracting histogram"
    path = os.path.join(sampleDataPath,exp)
    ## Give shell command to move to correct path
    
    ## Look for Exp folder
    if not os.path.exists(outputDataPath + exp):
        os.makedirs(outputDataPath + exp)

    ##Create an output file with the metric name.
    FILE = open(outputDataPath + exp + "/" + aMetric + ".js","w")
    
    ##Grep for the given metric 
    grepRes = subprocess.Popen('cd '+ path + ' ;' + 'grep -ris \\"'+ aMetric + '\\" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   
    ## Open json object
    FILE.write("datatest[\""+exp+"\"] = [" )
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


def extractScatterplotMetricFromExperiment(exp, aMetric):
    print "EXTracting histogscatterrrrram"
    basePath = os.path.join(sampleDataPath, exp)
    ## Give shell command to move to correct path
    
    benchmarksProcess = subprocess.Popen("cd "+basePath+"; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);  
      
    for line in benchmarksProcess.stdout.readlines():
        tokens = line.split(" ")
        benchmarkname= tokens[0].rstrip("\n")
    
        ##Grep for the given metric 
        grepRes = subprocess.Popen('cd '+ basePath+"/"+benchmarkname + '; grep -ris "'+ aMetric + '" *', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       
        ## Look for Exp folder
        if not os.path.exists(outputDataPath + exp +"/"+benchmarkname):
            os.makedirs(outputDataPath + exp +"/"+benchmarkname)
    
        ##Create an output file with the metric name.
        FILE = open(outputDataPath + exp + "/" + benchmarkname + "/" + aMetric + ".js","w")
       
        ## Open json object
        FILE.write("datatest[\"" + exp + benchmarkname + "\"] =" )
        
        ##Parse and write data
        for dataline in grepRes.stdout.readlines():
            dataArray = dataline[dataline.index('['):dataline.index(']')+1];
            FILE.write(dataArray)
            
    
        FILE.write(";")
        FILE.close()

    
        
        


