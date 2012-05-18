from simulation.settings import EXP_ROOT_DIR, EXECUTABLE_PATH
import os, datetime, sys
from models import Benchmarks, ExtendedExperimentTypes, Experiments, BenchmarkSuite
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
        extExp = ExtendedExperimentTypes.objects.all();
        extExpExcl = sepByComma(request.POST['as_values_3'])
        for ext in extExp:
            if ext == "": continue
            if str(ext.expType) not in extExpExcl:
                curexpName = request.POST['size_pref'] + "_" + base + "_" + str(ext.expType)
                curExpDir = dirName + os.sep + "data" + os.sep + curexpName
                os.makedirs(curExpDir)
                
                #Prepare the arguments for the experiment
                curArg = convertTypeToArgs(request.POST['common'].strip(), request.POST['size'],
                                request.POST['pcm_options'], base)
                curArg = addExtensions(curArg, str(ext.expType))
    
                #Save current experiment to database
                saveExperiment(request, curexpName, fileName, curArg)

                #Go through benchmarks in suite and write out
                exclBench = sepByComma(request.POST['as_values_1'])
                bsuite = request.POST['benchsuite']
                bmarks = Benchmarks.objects.filter(suite=getBenchmarkSuiteId(bsuite))
                for bmark in bmarks:
                    if bmark.name not in exclBench:
                        for arg in curArg:
                            f.write('Arguments = ' + bsuite + " " + bmark.name + " " + dirName
                                    + " " + curExpDir + " " + fileName + " " + arg + "\n")
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
    experiment = Experiments.get_or_create(submissionName = request.POST['expName'], expName = curexpName)
    experiment.subdate = datetime.datetimenow()
    experiment.binrev = fileName
    experiment.bsuite = BenchmarkSuite.objects.get(suite=request.POST['benchsuite'])
    experiment.argset = curArg
    experiment.rootDirectory = os.path.join(EXP_ROOT_DIR, request.POST['expName'], curexpName)
    experiment.save()
    exclBench = sepByComma(request.POST['as_values_1'])
    for bench in exclBench:
        if bench != "": 
            curBench = Benchmarks.objects.get(name=bench)
            experiment.exclBench.add(curBench)
    
###############################################################
# Convert experiment type to args
###############################################################
def convertTypeToArgs(baseArgs, size, pcm_options, expType):
    #Set up args arguments
    args = baseArgs + " "
    args = args.replace("#{size}", size)
    
    #Generate argument option based on expType and return
    if expType == 'pcm':
        args = args + pcm_options + "-pref false"
    elif expType == 'stream_pcm':
        args = args + pcm_options + "-pref_stride false -pref_stream true"
    elif expType == 'np':
        args = args + "-pref false"
    elif expType == 'stream':
        args = args + "-pref_stride false -pref_stream true"
    elif expType == 'stream_shallowfront':
        args = args + "-pref_stride false -pref_stream true -core_decode_stages 1 -core_map_stages 1"
    elif expType == 'np_perfbp':
        args = args + "-pref false -perfect_bp true"
    elif expType == 'stream_perfbp':
        args = args + "-pref_stride false -pref_stream true -perfect_bp true"
    elif expType == 'stream_smallrob':
        args = args + "-core_rob_size 40 -core_sched_size 20"
    elif expType == 'stream_inorder':
        args = args + "-core_width 1 -core_fetch_stages 2 -core_decode_stages 2 -core_map_stages 2 -core_rob_size 16 -core_sched_size 1"
    elif expType == 'stream_smallrob_perfbp':
        args = args + "-core_rob_size 40 -core_sched_size 20 -perfect_bp true"
    elif expType == 'stream_inorder_perfbp':
        args = args + "-core_width 1 -core_fetch_stages 2 -core_decode_stages 2 -core_map_stages 2 -core_rob_size 16 -core_sched_size 1 -perfect_bp true"
    elif expType == 'stream_longlat':
        args = args + "-pref_stride false -pref_stream true -mem_multiplier 64"
    elif expType == 'stream_newsys':
        args = args + "-pref_stride false -pref_stream true -mem_multiplier 16 -mem_channels 0 -mem_ranks_per_chan 0 -mem_banks_per_rank 3 -core_decode_stages 3 -core_map_stages 2"
    elif expType == 'np_newsys':
        args = args + "-pref false -mem_multiplier 8 -mem_channels 0 -mem_ranks_per_chan 0 -mem_banks_per_rank 3 -core_decode_stages 3 -core_map_stages 2"
    elif expType == 'stream_newsys2':
        args = args + "-pref_stride false -pref_stream true -core_decode_stages 3 -core_map_stages 2"
    elif expType == 'np_newsys2':
        args = args + "-pref false -core_decode_stages 3 -core_map_stages 2"
    return args + " "

###############################################################
# Add experimental extensions
###############################################################
def addExtensions(args, extType):
    args = args.strip()
    retArgs = []
    if extType == 'base':
        retArgs.append(args)
    elif extType == 'ra':
        retArgs.append(args + "-core_ra true -ra_slicestats true")
    elif extType == 'rai':
        retArgs.append(args + "-core_ra true -ra_inhibit_flushcost true -ra_inhibit_flushcost_misp 3")
    elif extType == "ralim":
        for i in range (1, 9):
            iVal = str(i)
            retArgs.append(args + "-core_ra true -ra_miss_limit " + iVal)
    elif extType == "effra_overlap0.5":
        retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap_T 0.5")
    elif extType == "effra_overlap0.0":
        retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap false")
    elif extType == "effra":
        retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap_T 1.0 -core_ra_efficient_nofp false")
    elif extType == "effra_fp":
        retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap_T 1.0 -core_ra_efficient_nofp true")    
    elif extType == "limited_effra":
        for i in range (1, 9):
            retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap_T 1.0 -core_ra_efficient_nofp false -ra_miss_limit " + str(i))   
    elif extType == "limited_effra_fp":
        for i in range (1, 9):
            retArgs.append(args + "-core_ra_efficient true -core_ra_efficient_overlap_T 1.0 -core_ra_efficient_nofp true -ra_miss_limit " + str(i))   
    elif extType == "ra_randdrop_0.01":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.01") 
    elif extType == "ra_randdrop_0.02":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.02")
    elif extType == "ra_randdrop_0.05":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.05")
    elif extType == "ra_randdrop_0.1":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.1")
    elif extType == "ra_randdrop_0.2":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.2")    
    elif extType == "ra_randdrop_0.5":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 0.5")     
    elif extType == "ra_randdrop_1.0":
        retArgs.append(args + "-core_ra_random_drop true -ra_slicestats true -core_ra_random_drop_P 1.0")  
    elif extType == "sa3":
        retArgs.append(args + "-core_sa_dataflow3 true -core_sa_repeat true -core_sa_tryra false")
    elif extType == "sa4":
        retArgs.append(args + "-core_sa_dataflow4 true")
    elif extType == "coarsefilt":
        retArgs.append(args + "-core_ra_coarsefilt true -core_ra_coarsefilt_ld_allpaths true  -core_ra_coarsefilt_drop_ends_period true -core_ra_coarsefilt_trainalways true")
    elif extType == "probfilt4_perfect":
        retArgs.append(args + "-core_ra_probfilt4 true -core_ra_probfilt4_perfectdrops true -core_ra_probfilt4_dropfile EXPDIR/ndrop/BENCH.ndrop")
    elif extType == "probfilt5":
        retArgs.append(args + "-core_ra_probfilt5 true")
    elif extType == "probfilt5_effra":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_efficient true -core_ra_efficient_nofp false")
    elif extType == "probfilt5_effra_fp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_efficient true -core_ra_efficient_nofp true")
    elif extType == "probfilt5_dropflux":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_dropflux_filter true")
    elif extType == "probfilt5_dropflux_effra":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_dropflux_filter true -core_ra_efficient true -core_ra_efficient_nofp false")
    elif extType == "probfilt5_dropflux_effra_fp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_dropflux_filter true -core_ra_efficient true -core_ra_efficient_nofp true")
    elif extType == "probfilt5_droptable":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true")
    elif extType == "probfilt5_droptable":
        for i in range(1, 9):
            retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -ra_miss_limit " + str(i))
    elif extType == "probfilt5_droptable_trainalways":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_effra":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_efficient true -core_ra_efficient_nofp false")
    elif extType == "probfilt5_droptable_effra_fp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_efficient true -core_ra_efficient_nofp true")
    elif extType == "probfilt5_droptable_dropflux":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true")
    elif extType == "probfilt5_droptable_dropflux_trainalways":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_dropflux_effra":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_efficient true -core_ra_efficient_nofp false")
    elif extType == "probfilt5_droptable_dropflux_effra_fp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_efficient true -core_ra_efficient_nofp true")
    elif extType == "probfilt5_droptable_dropflux_leadtable":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_leadtable true")
    elif extType == "probfilt5_droptable_dropflux_trainalways_leadtable":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_leadtable true -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_rdp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_rdit true")
    elif extType == "probfilt5_droptable_dropflux_rdp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_rdit true")
    elif extType == "probfilt5_droptable_rdp2":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_rdit true -core_ra_probfilt5_rdit_ddt 64")
    elif extType == "probfilt5_droptable_dropflux_rdp2":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_rdit true -core_ra_probfilt5_rdit_ddt 64")
    elif extType == "probfilt5_droptable_trainalways_rdp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_rdit true -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_dropflux_trainalways_rdp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_rdit true -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_trainalways_rdp2":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_rdit true -core_ra_probfilt5_rdit_ddt 64 -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_droptable_dropflux_trainalways_rdp2":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_droptable true -core_ra_probfilt5_droptable_size 65536 -core_ra_probfilt5_droptable_tagged true -core_ra_probfilt5_dropflux_filter true -core_ra_probfilt5_rdit true -core_ra_probfilt5_rdit_ddt 64 -core_ra_probfilt5_trainalways true")
    elif extType == "probfilt5_alldrop":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_drop_all true")
    elif extType == "ra_rdp":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_disable_drop true -core_ra_probfilt5_rdit true")
    elif extType == "ra_rdp2":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_disable_drop true -core_ra_probfilt5_rdit true -core_ra_probfilt5_rdit_ddt 64")
    elif extType == "ra_leadtable":
        retArgs.append(args + "-core_ra_probfilt5 true -core_ra_probfilt5_disable_drop true -core_ra_probfilt5_leadtable true")
    return retArgs

###############################################################
# sepByComma
###############################################################
def sepByComma(value):
    return [x.strip() for x in value.split(",")]
