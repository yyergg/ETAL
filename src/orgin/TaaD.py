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

import sys
import time
import json
import os
import Config
from TaaDTCG import TestCaseGenerator2
from TestingTask import TestingTask
from AdbExecutor import AdbExecutor
from abstraction import Abstraction


def generateTrace(taskSetting,gen,task,adb):
    # 4. parse Task
    traceLength = taskSetting["traceLength"]
    traceAmount = taskSetting["traceAmount"]
    sleepTime = taskSetting["sleepTime"]
    appPackageName= taskSetting["appPackageName"]
    homePackageName = taskSetting["homePackage"]

    # 5. generate trace
    for i in range(0,traceAmount):
        # 6. Reset and get the beginning State before each trace
        task._TestingTask__newTrace()
        adb.restartAPP()
        xml = adb.dumpXML(i+1,0)
        nextAction = None
        isPass = True

        traceFile = task._TestingTask__updateAutomata(i+1,0,xml,"XML")

        for j in range(0,traceLength):
            # 7. get test input
            if nextAction == None:
                action = gen.getTestInput(task)
            else:
                action = nextAction
                nextAction = None

            if action == None:
                print("Action is None, continue next step.")
                continue

            # 8. execute adb command, including mem, coverage,png
            print("action = ",action)
            result = adb.execute(action,i+1,j+1)

            # 9. waiting the devices to a stable state
            time.sleep(sleepTime)

            if result == "failed":
                print("Action failed.")
                return
            elif result == "illegal":
                print("Action is illegal.")
                continue
            elif result == "terminate":
                print("Terminate this trace.")
                break
            elif result == "restart":
                print("Restart application.")
                adb.restartAPP()
                xml = adb.dumpXML(i+1,j+1)
                task._TestingTask__updateAutomata(i+1,j+1,xml,"Restart")
                continue
            else:
                # 10. get current XML, and check if app is crashed
                xml = adb.dumpXML(i+1,j+1)

                packageResult = checkPackage(xml,appPackageName,homePackageName)
                if packageResult != "samePackage":
                    if action[0] == "keyevent" or packageResult == "differentPackage":
                        nextAction = task.getCurrentState().getRestartKey()
                        print("Restart app since left app by keyevent or to the other app.")

                    elif packageResult == "homePackage":
                        task._TestingTask__updateAutomata(i+1,j+1,action,"Action")
                        task._TestingTask__updateAutomata(i+1,j+1,xml,"XML")
                        print("Terminate app since back to the home screen.")
                        isPass = False
                        break
                csResult = checkCallStack(adb.getLogPath())
                if csResult != "pass":
                    isPass = False
                    break

                # 11. update Automata by XML and action
                task._TestingTask__updateAutomata(i+1,j+1,action,"Action")
                task._TestingTask__updateAutomata(i+1,j+1,xml,"XML")

        # 12. End of a trace, and start writing trace.txt file.
        if isPass == True:
            with open(traceFile,"a") as trace:
                trace.write("pass\n")
        else:
            with open(traceFile,"a") as trace:
                trace.write("fail\n")
                if csResult != "pass":
                    trace.writelines(csResult)

        print("")

    # 13.End of generating traces, and start saving the session automata
    task._TestingTask__saveSessionAutomata()


def checkPackage(Path,appPackageName,homePackage):
    import xml.etree.ElementTree as ET
    xml = ET.parse(Path)
    root = xml.getroot()

    # package name is different
    if root[0].attrib["package"] != appPackageName:
        if root[0].attrib["package"] == homePackage:
            return "homePackage"
        else:
            return "differentPackage"

    else: return "samePackage"

def checkCallStack(log):
    logFile = open(log,"r")
    form = logFile.readlines()
    logFile.close()

    for line in form[:]:
        if line.startswith("--------- beginning"):
            form.remove(line)
        if line == "\n":
            form.remove(line)

    if len(form) != 0:
        print("Fail : Call stack = ")
        print(form)
        return form
    else:
        print("Call stack check pass.")
        return "pass"





def main():
    rootDir = Config.getRoot()
    # 1. load task json
    taskSetting_json = open(os.path.join(rootDir,"testcase",sys.argv[1]))
    taskSetting = json.load(taskSetting_json)
    taskSetting_json.close()

    #For TraceCollector
    if taskSetting["component"] == "TraceCollector":
        # 2. get abstraction setting and generate new TestingTask, task
        abstraction = Abstraction()
        absSetting = abstraction.absSettingParse(taskSetting)
        abstraction.setAbstraction(absSetting)
        adb = AdbExecutor(taskSetting,absSetting)
        task = TestingTask(abstraction,adb)

        # 3. generate new TestCaseGenerator, gen
        if taskSetting["algorithm"] == "monkey":
            from TestCaseGenerator import Monkey
            gen = Monkey()

        if taskSetting["algorithm"] == "DFS":
            from TestCaseGenerator import DFS
            gen = DFS()

        if taskSetting["algorithm"] == "SELabeler":
            from SpecElicitor.SpecElicitorAdapter import SpecElicitorAdapter
            #root = "/home/misgood/workspace/taad"
            root = os.path.dirname(os.path.realpath(__file__))
            user = taskSetting["userName"]
            app = taskSetting["appPackageName"]
            parentPath = os.path.join(root,user,app)
            gen = SpecElicitorAdapter(task, parentPath)

        if taskSetting["algorithm"] == "TestCaseGenerator2":
            failFile = open("FailRule.txt")
            gen = TestCaseGenerator2(task)

        generateTrace(taskSetting,gen,task,adb)

    # For AutomataGenerator
    elif taskSetting["component"] == "AutomataGenerator":
        if taskSetting["algorithm"] == "VersionAutomata":
            from AutomataGenerator import VersionAutomata
            gen = VersionAutomata(taskSetting)
            gen.generateAutomata()




if __name__ == '__main__':
    main()



