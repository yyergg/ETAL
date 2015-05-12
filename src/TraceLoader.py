import os
import sys
import re

class TraceLoader:
    listTraces = []
    pathTraceFolder = ""

    def loadTrace(self,pathTraceFolder):
        self.pathTraceFolder = os.path.join(os.getcwd(), pathTraceFolder)
        listTraces = []

        for root, dirs, files in os.walk(self.pathTraceFolder):
            for filename in files:
                infile = open(os.path.join(root,filename), 'r')
                lines = infile.readlines()
                infile.close()
                regexState = re.compile(r'(?<=state\_)[0-9]+(?=\.)')
                regexClick = re.compile(r'(?<=CLICK\:)[0-9]+(?=\s)')
                newTrace = []
                preState = ""
                for line in lines:
                    if line.find("CLICK") != -1:
                        if preState == "":
                            print("Error: Click before any state in", os.path.join(root,filename))
                        newTrace.append(preState+"_"+regexClick.search(line).group(0))
                    elif line.find("state_") != -1:
                        preState = regexState.search(line).group(0)
                        newTrace.append(preState)
                    elif line.find("error free") != -1:
                        newTrace.append("Pass")
                    else:
                        newTrace.append("Fail")
                        break
                self.listTraces.append(newTrace)

    def printTrace(self):
        for trace in self.listTraces:
            s = ""
            for event in trace:
                s = s+event+" "
            print(s)