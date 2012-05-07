from simulation.settings import EXP_ROOT_DIR, EXECUTABLE_PATH
import os, datetime

'''
 Responsible for converting dictionary inputs into log file,
 create corresponding directory, and connect to condor to run
 experiment
'''
def generate(self, request):
    dirName = decideName()
    makeCondorSub(request, dirName)
    
'''
 Decide on directory name to create for this experiment
 Use the date and add number from 1 upward
'''
def decideName(self):
    curDate = datetime.datetime.now()
    curMonth = "%02d" % curDate.month
    curDay = "%02d" % curDate.day
    baseName = str(curDate.year) + curMonth + curDay
    
    #Loop until a folder that does not exist is found.
    #Create that folder and break
    i = 0
    while True:
        curDir = EXP_ROOT_DIR + os.sep + baseName + "_" + str(i)
        if not os.path.isdir(curDir):
            os.mkdir(curDir)
            return curDir
            break
        i = i + 1

'''
 Creae condor.sub file
'''
def makeCondorSub(self, request, dirName):
    #Open condor.sub file
    filePath = dirName + os.sep + "condor.sub"
    f = open(filePath,"w")
    
    #Write Header
    f.write("Universe = vanilla\n")
    if request.POST.has_key('useOut'):
        f.write(dirName + os.sep + "log" + os.sep + "$(cluster).$(process).out\n")
    if request.POST.has_key('useErr'):
        f.write(dirName + os.sep + "log" + os.sep + "$(cluster).$(process).err\n")
    if request.POST.has_key('useLog'):
        f.write(dirName + os.sep + "log" + os.sep + "$(cluster).$(process).log\n")
    f.write("Initialdir = " + dirName + "\n")
    f.write("Executable = " + EXECUTABLE_PATH + "\n")
    f.write("\n")

    #Write requirements
    f.write("Requirements = ((")
    for i in range(0,10):
        f.write("(Machine == \"ece00" + str(i) + ".ece.cmu.edu\") || ")
    for i in range(10,31):
        f.write("(Machine == \"ece0" + str(i) + ".campus.ece.cmu.local\") || ")
    f.write("Machine == \"ece031.campus.ece.cmu.local\")) || SAFARI_COMPUTE == True || SCOTCH_CLUSTER == True))\n")
    f.write("\n")

    #Generate benchmark list
    
