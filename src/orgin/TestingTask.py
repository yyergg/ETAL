#-------------------------------------------------------------------------------
# N__ame:        ?????1
# Purpose:
#
# Author:      b9890_000
#
# Created:     08/01/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import AutomataManager
import os

class TestingTask:
    def __init__(self,abstraction,adbExec):
        print("testing task init")
        self.__adbExec = adbExec
        self.__fileManager = self.__adbExec.getFileManager()
        self.__am = AutomataManager.AutomataManager(abstraction)

        self.versionNum = self.__fileManager.getVersionNum()
        self.abstractionNum = self.__fileManager.getAbstractionNum()
        self.sessionNum = self.__fileManager.getSessionNum()

        self.traceSetDir = self.__fileManager.getTraceSetDir()
        self.currentStateID = 0

    '''
    The followings are private functions that you should not use.
    '''
    def __updateAutomata(self,traceNum,step,file,mode):
        self.currentTraceNum = traceNum
        self.currentStep = step
        stepID = (self.versionNum,self.abstractionNum,self.sessionNum,traceNum,step)
        traceFile = os.path.join(self.traceSetDir,str(traceNum),"trace.txt")

        if mode == "XML":
            print("update xml")
            self.currentStateID = self.__am.updateAutomataByXML(file,stepID,self.__adbExec.getMemInfo())

            with open(traceFile,"a") as trace:
                trace.write("uidump"+str(step)+".xml => state"+str(self.currentStateID)+"\n")

        elif mode == "Action":
            print("update action")
            self.currentStateID = self.__am.updateAutomataByAction(file,stepID)

            with open(traceFile,"a") as trace:
                trace.write(" move"+str(step)+".json => state"+str(self.currentStateID)+"\n")

        elif mode == "Restart":
            print("update restart")
            self.currentStateID = self.__am.updateAutomataByRestart(file,stepID,self.__adbExec.getMemInfo())

            with open(traceFile,"a") as trace:
                trace.write(" move"+str(step)+".json => restart -1\n")
                trace.write("uidump"+str(step)+".xml => state"+str(self.currentStateID)+"\n")

        return traceFile

    def __newTrace(self):
        print("new trace")
        self.__am.newTrace()

    def __saveSessionAutomata(self):
        self.__am.saveAutomata(self.getSessionAutomataDir())


    '''
    The following is getting the data structure related to the Automata.
    '''
    def getAutomata(self):
        return self.__am.getAutomata()

    def getTrace(self):
        return self.__am.getTrace()

    def getCurrentState(self):
        return self.__am.getCurrentState()

    # parent path is like: os.path.join(root,userName,appPackageName)
    def setParentPath(self,path):
        self.__am.setParentPath(path)

    # set parent path before you call this function
    def getAutomataByDir(self,dir,algo):
        return self.__am.loadAutomata(dir,algo)


    '''
    The following is getting the file path you need.
    '''
    def getMemPath(self):
        return self.__adbExec.getMemPath()

    def getCoveragePath(self):
        return self.__adbExec.getCoveragePath()

    def getPngPath(self):
        return self.__adbExec.getPngPath()


    '''
    The following is getting the directory you need.
    '''
    def getApkDir(self):
        return self.__fileManager.getApkDir()

    def getVersionDir(self):
        return self.__fileManager.getVersionDir()

    def getTraceSetDir(self):
        return self.__fileManager.getTraceSetDir()

    def getSessionAutomataDir(self):
        return self.__fileManager.getSessionAutomataDir()

    def getLabeledTraceDir(self):
        return self.__fileManager.getLabeledTraceDir()

    '''
    The following is getting the system information
    '''
    def getCoverageInfo(self):
        return self.__adbExec.getCoverageInfo()

    def getMemoryInfo(self):
        return self.__adbExec.getMemInfo()

    '''
    Others you can get.
    '''
    def getCurrentStep(self):
        return (self.currentTraceNum,self.currentStep)

    def getAppName(self):
        return self.__adbExec.appPackageName



