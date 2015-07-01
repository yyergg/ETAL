#-------------------------------------------------------------------------------
# Name:        ?????1
# Purpose:
#
# Author:      b9890_000
#
# Created:     23/06/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import json
import shutil
import datetime


def getPngbyStepID(stepID,automataDir):
        versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
        png = os.path.join(os.path.dirname(automataDir),"test",str(traceNum),"screenShot"+str(stepNum)+".png")
        #print("png = ",png)
        return png

def getMovebyStepID(stepID,automataDir):
        versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
        move = os.path.join(os.path.dirname(automataDir),"test",str(traceNum),"move"+str(stepNum)+".json")
        #print("move = ",move)
        return move

def getStatePath(automataDir,state):
    return os.path.join(automataDir,"state"+str(state)+".json")

def genReport(traceFile,automataDir):
    print(traceFile,automataDir)
    stateList = []
    traceNum = 0
    now = datetime.datetime.now()

    with open(traceFile,'r') as data:
        traces = data.readlines()
        traceNum = len(traces)
        i = 0
        for trace in traces:
            reportDir = str(now).split(".")[0].replace(":","_")+"_trace"+str(i)
            os.mkdir(reportDir)
            stateNum = 0
            moveNum = 1
            for state in trace.split():
                stateFile = getStatePath(automataDir,state)
                state_json = open(stateFile)
                stateData = json.load(state_json)
                state_json.close()

                if stateData["stateType"] == "View":
                    png = getPngbyStepID(stateData["stateXMLs"][0],automataDir)
                    shutil.copy(png,".") # copy to current directory
                    shutil.move(os.path.basename(png),os.path.join(reportDir,str(stateNum)+".png")) # rename the png file
                    print("png = ",png)
                    stateNum += 1
                else:
                    move = getMovebyStepID(stateData["stateMoves"][0],automataDir)
                    move_json = open(move)
                    moveData = json.load(move_json)
                    move_json.close()
                    print("adb = ",moveData["adbCommand"])
                    with open(os.path.join(reportDir,"move"+str(moveNum)+".txt"),'w') as moveFile:
                        moveFile.write(moveData["adbCommand"])

                    moveNum += 1

            i += 1


def main():
    traceFile = sys.argv[1]
    automataDir = sys.argv[2]

    genReport(traceFile,automataDir)


if __name__ == '__main__':
    main()
