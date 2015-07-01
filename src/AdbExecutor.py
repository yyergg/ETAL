#-------------------------------------------------------------------------------
# Name:        ?????1
# Purpose:
#
# Author:      b9890_000
#
# Created:     08/01/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import shutil
import time
import json
from FileManager import FileManager
from Instrumentor import Instrumentor
from Coverage import CoverageInformation
from Memory import MemoryInformation

class AdbExecutor:
    def __init__(self,taskSetting,absSetting):
        self.userName = taskSetting["userName"]
        self.appPackageName = taskSetting["appPackageName"]
        self.firstActivityName = taskSetting["firstActivityName"]
        self.serialNumber = taskSetting["serialNumber"]
        self.algorithm = taskSetting["algorithm"]
        self.fileManager = FileManager(taskSetting,absSetting)
        self.fileManager.initialize()
        self.instrumentor = Instrumentor(taskSetting,self.fileManager.getVersionDir())
        self.instrumentor.instrument()
        self.coverageInfo = CoverageInformation(self.fileManager.getVersionDir(),self.instrumentor.isInstrument())
        self.meminfo = MemoryInformation()
        self.xmlPath = ""
        self.memPath = ""
        self.coveragePath = ""
        self.pngPath = ""
        self.actionType = "restart"
        self.actionView = None
        self.actionArgu = None

    '''
    The followings are functions getting the all possible files' path in trace
    '''
    def getMemPath(self):
        return self.memPath

    def getCoveragePath(self):
        return self.coveragePath

    def getPngPath(self):
        return self.pngPath

    def getLogPath(self):
        return self.logPath

    '''
    Return the file manager
    '''
    def getFileManager(self):
        return self.fileManager

    '''
    Return system information
    '''
    def getMemInfo(self):
        return self.meminfo

    def getCoverageInfo(self):
        return self.coverageInfo

    '''
    Dump xml file, png file, memory file, coverage file, and caculate coverage
    '''
    def dumpXML(self,traceNum,step):
        traceSetDir = self.fileManager.getTraceSetDir()
        traceNumDir = os.path.join(traceSetDir,str(traceNum))
        # generate each trace directory
        self.fileManager.mkdir(traceNumDir)

        # generate trace.txt
        if not os.path.isfile(os.path.join(traceNumDir,"trace.txt")):
            with open(os.path.join(traceNumDir,"trace.txt"),"w") as trace:
                trace.write("")

        # generate log.txt
        self.logPath = os.path.join(traceNumDir,"log"+str(step)+".txt")
##        print(self.logPath)
        os.system("adb -s "+self.serialNumber+" logcat -d AndroidRuntime:E "+self.appPackageName+":D *:S > "+self.logPath)
##        print("!!")
        # support dump xml file
        os.system("adb -s "+self.serialNumber+" shell /system/bin/uiautomator dump /sdcard/uidump.xml")
        self.xmlPath = os.path.join(traceNumDir,"uidump"+str(step)+".xml")
        os.system("adb -s "+self.serialNumber+" pull /sdcard/uidump.xml "+self.xmlPath)

        # support memory information
        self.memPath = os.path.join(traceNumDir,"memoryInfo"+str(step)+".txt")
        os.system("adb -s "+self.serialNumber+" shell dumpsys meminfo "+self.appPackageName+" > "+self.memPath)

        # support line coverage
        self.coveragePath = os.path.join(traceNumDir,"step"+str(step)+"_covered_line.txt")
        os.system("adb -s "+self.serialNumber+" logcat -d System.out:I *:S > "+self.coveragePath)
        os.system("adb -s "+self.serialNumber+" logcat -c")

        # support screen shot
        os.system("adb -s "+self.serialNumber+" shell screencap -p /sdcard/dump.png")
        self.pngPath = os.path.join(traceNumDir,"screenShot"+str(step)+".png")
        os.system("adb -s "+self.serialNumber+" pull /sdcard/dump.png "+self.pngPath)

        time.sleep(1)

        # caculate coverage information
        self.coverageInfo.caculate(self.coveragePath)

        # caculate memory usage
        self.meminfo.parse(self.memPath)

        return self.xmlPath

    def execute(self,action,traceNum,step):
        # Possible actions are ("click",view,(x1,y1)),("text",view,"a random string"),("roll",view,(dx,dy))
        # and ("keyevent",None,(a random system key,"it's meaning"))

        self.actionType = action[0]
        self.actionView = action[1]
        self.actionArgu = action[2]
        traceSetDir = self.fileManager.getTraceSetDir()
        traceNumDir = os.path.join(traceSetDir,str(traceNum))

        movePath = os.path.join(traceNumDir,"move"+str(step)+".json")

        # record the data stored in move.json
        data = {'actionType':self.actionType}
        if self.actionView == None or self.actionView == "None":
            data['targetViewAttributes'] = "None"
            data['layer'] = -1
            data['index'] = -1
        else:
            data['targetViewAttributes'] = self.actionView.attrDict
            data['layer'] = self.actionView.getLayer()
            data['index'] = self.actionView.getIndex()
        data['actionArgu'] = self.actionArgu

        # execute the command
        doCommand = False
        adb = "adb -s "+self.serialNumber+" shell input "
        if self.actionType == "click":
            # adb shell input tap 250 250
            adb = adb + "tap " + str(self.actionArgu[0]) + " " + str(self.actionArgu[1])
            doCommand = True

        elif self.actionType == "text":
            # adb shell input text abcdefg
            adb = adb + "text " + str(self.actionArgu)
            doCommand = True

        elif self.actionType == "roll":
            # adb shell input roll 10 10
            adb = adb + "roll " + str(self.actionArgu[0]) + " " + str(self.actionArgu[1])
            doCommand = True

        elif self.actionType == "keyevent":
            # adb shell input keyevent 4
            adb = adb + "keyevent " + str(self.actionArgu[0])
            doCommand = True

        elif self.actionType == "terminate":
            # terminate this trace
            adb = "terminate"

        elif self.actionType == "restart":
            # restart the application
            adb = "restart"

        else:
            adb = "illegal"
            self.actionType = "illegal"

        data["adbCommand"] = adb
        with open(movePath, "w") as outfile:
            json.dump(data, outfile, indent=4)

        if doCommand:
            os.system(adb) # execute adb command

        return self.actionType

    def restartAPP(self):
        #os.system("adb root")
        os.system("adb -s "+self.serialNumber+" shell am force-stop "+self.appPackageName)
        os.system("adb -s "+self.serialNumber+" shell am start "+self.appPackageName+"/"+self.firstActivityName)
        time.sleep(4)











