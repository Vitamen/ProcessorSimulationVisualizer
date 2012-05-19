from simulation.settings import EXP_ROOT_DIR, EXECUTABLE_PATH
import os, datetime, sys
from models import Benchmarks, BaseExperiment, ExtExperiment , Experiments, BenchmarkSuite
from simulation.condorManager import CondorManager

###############################################################
# getBenchmarkSuite
###############################################################
def getBenchmarkSuiteId(bsuite):
    if bsuite == 'speccpu': return 1
    elif bsuite == 'spec2006': return 2
    
###############################################################
# Responsible for converting dictionary inputs into log file,
# create corresponding directory, and connect to condor to run
# experiment
###############################################################
def generate(request):
    #Set up directory
    baseDir = request.POST['expName']
    dirName = EXP_ROOT_DIR + os.sep + baseDir
    binName = dirName + os.sep + "bin"
    dataName = dirName + os.sep + "data"
    logName = dirName + os.sep + "log"
    os.mkdir(dirName)
    os.mkdir(binName)
    os.mkdir(dataName)
    os.mkdir(logName)   
    
    #Upload chosen binary file to folder
    if 'binFile' in request.FILES:
        myFile = request.FILES['binFile']
        fd = open(binName + os.sep + myFile.name, 'wb')
        line = myFile.readline()
        result = ""
        while line:
            result = result + line
            line = myFile.readline()
        fd.write(result)
        fd.close()
            
    #Generate condor.sub
    fileName = myFile.name
    makeCondorSub(request, fileName, dirName)
    
    #Return path to generated condor.sub file
    return dirName + os.sep + "condor.sub"
    
###############################################################
# Decide on directory name to create for this experiment
# Use the date and add number from 1 upward
###############################################################
def decideName():
    curDate = datetime.datetime.now()
    curMonth = "%02d" % curDate.month
    curDay = "%02d" % curDate.day
    baseName = str(curDate.year) + curMonth + curDay
    
    #Loop until a folder that does not exist is found.
    #Create that folder and break
    i = 0
    while True:
        baseDir = baseName + "_" + str(i)
        curDir = EXP_ROOT_DIR + os.sep + baseDir
        if not os.path.isdir(curDir):
            return baseDir
            break
        i = i + 1

###############################################################
# Creae condor.sub file
###############################################################
def makeCondorSub(request, fileName, dirName):
    #Open condor.sub file
    filePath = dirName + os.sep + "condor.sub"
    f = open(filePath, "w")
    
    #Write Header
    f.write("Universe = vanilla\n")
    if request.POST.has_key('useOut'):
        f.write("Output = " + dirName + os.sep + "log" + os.sep + "$(cluster).$(process).out\n")
    if request.POST.has_key('useErr'):
        f.write("Error = " + dirName + os.sep + "log" + os.sep + "$(cluster).$(process).err\n")
    if request.POST.has_key('useLog'):
        f.write("Log = " + dirName + os.sep + "log" + os.sep + "$(cluster).$(process).log\n")
    f.write("Initialdir = " + dirName + "\n")
    f.write("Executable = " + EXECUTABLE_PATH + "\n")
    f.write("\n")

    #Write requirements
    f.write("Requirements = ((")
    for i in range(0, 10):
        f.write("(Machine == \"ece00" + str(i) + ".ece.cmu.edu\") || ")
    for i in range(10, 31):
        f.write("(Machine == \"ece0" + str(i) + ".campus.ece.cmu.local\") || ")
    f.write("Machine == \"ece031.campus.ece.cmu.local\")) || SAFARI_COMPUTE == True || SCOTCH_CLUSTER == True))\n")
    f.write("\n")

    #Go through each type of base experiment
    baseExp = sepByComma(request.POST['as_values_2'])
    for base in baseExp:
        if base == "": continue
        #Go through each type of extended experiment
        extExp = ExtExperiment.objects.all();
        extExpExcl = sepByComma(request.POST['as_values_3'])
        for ext in extExp:
            print >>sys.stderr, ext.name
            if ext.name == "": continue
            if ext.name not in extExpExcl:
                curexpName = request.POST['size_pref'] + "_" + base + "_" + str(ext.name)
                curExpDir = dirName + os.sep + "data" + os.sep + curexpName
                os.makedirs(curExpDir)
                
                #Prepare the arguments for the experiment
                curArg = convertTypeToArgs(request.POST['common'].strip(), request.POST['size'], base)
                curArg = addExtensions(curArg, str(ext.name))
    
                #Save current experiment to database
                saveExperiment(request, curexpName, fileName, curArg)

                #Go through benchmarks in suite and write out
                exclBench = sepByComma(request.POST['as_values_1'])
                bsuite = request.POST['benchsuite']
                bmarks = Benchmarks.objects.filter(suite=getBenchmarkSuiteId(bsuite))
                for bmark in bmarks:
                    if bmark.name not in exclBench:
                        f.write('Arguments = ' + bsuite + " " + bmark.name + " " + dirName
                                    + " " + curExpDir + " " + fileName + " " + curArg)
                        f.write("Queue\n")
                        f.write("\n")
                        bFolder = curExpDir + os.sep + bmark.name
                        if not os.path.exists(bFolder):
                            os.mkdir(bFolder)
    f.close()

###############################################################
# Make condor.sub for resubmission
###############################################################
def makeResubmission(ids):
    #Get current running submission
    f = open(os.path.join(EXP_ROOT_DIR, "curExp"))
    val = f.readlines()
    if len(val) > 0: curExp = val[0]
    else: return
    
    #Extract the header from relevant condor.sub file
    #and write temporary submission
    origFile = os.path.join(EXP_ROOT_DIR, curExp, "condor.sub")
    tmpFile = os.path.join(EXP_ROOT_DIR, curExp, "condor.sub.tmp")
    f = open(origFile, "r")
    fp = open(tmpFile, "w")
    line = f.readline()
    while line:
        fp.write(line)
        if "Requirements" in line: break
        line = f.readline()
        
    #Use CondorManager to get the long status of ids & write
    manage = CondorManager.Manager()
    for curId in ids:
        retVal = manage.getStatusLong(curId)
        arg = findArgument(retVal)
        fp.write("Arguments = " + arg + "\n")
        fp.write("Queue\n\n")
    f.close()
    fp.close()
    return tmpFile

###############################################################
# Find argumetn from retVal
###############################################################
def findArgument(retVal):
    lines = retVal.split("\n")
    for line in lines:
        if "Arguments" in line:
            arg = line[line.index(' = "')+5:-1]
            return arg
        
###############################################################
# Save experiment to database
###############################################################
def saveExperiment(request, curexpName, fileName, curArg):
    experiment = Experiments(submissionName = request.POST['expName'], expName = curexpName)
    experiment.subdate = datetime.datetime.now()
    experiment.binrev = fileName
    experiment.bsuite = BenchmarkSuite.objects.get(suite=request.POST['benchsuite'])
    experiment.argset = curArg
    experiment.rootDirectory = os.path.join(EXP_ROOT_DIR, request.POST['expName'], curexpName)
    experiment.save()
    print >>sys.stderr, experiment
    exclBench = sepByComma(request.POST['as_values_1'])
    for bench in exclBench:
        if bench != "": 
            curBench = Benchmarks.objects.get(name=bench)
            experiment.exclBench.add(curBench)
    
###############################################################
# Convert experiment type to args
###############################################################
def convertTypeToArgs(baseArgs, size, expType):
    #Set up args arguments
    args = baseArgs + " "
    args = args.replace("#{size}", size)
    
    #Get model for base experiment types
    baseModel = BaseExperiment.objects.get(name=expType)
    args = args + baseModel.value
    return args

###############################################################
# Add experimental extensions
###############################################################
def addExtensions(args, extType):
    args = args + " "
    extModel = ExtExperiment.objects.get(name=extType)
    args = args + extModel.value
    return args

###############################################################
# sepByComma
###############################################################
def sepByComma(value):
    return [x.strip() for x in value.split(",")]
