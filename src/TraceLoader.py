import os
import sys
import re

class TraceLoader:
    listTraces = []
    clusteredTraces = {}
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
                            print("Error: Click before any state. In", os.path.join(root,filename))
                        newTrace.append(preState+"_"+regexClick.search(line).group(0))
                    elif line.find("state_") != -1:
                        preState = regexState.search(line).group(0)
                        newTrace.append(preState)
                    elif line.find("error free") != -1:
                        self.listTraces.append((newTrace, "Pass"))
                        break
                    else:
                        self.listTraces.append((newTrace, "Fail"))
                        break
                

    def clusterTraces(self):
        #seperate Pass/Fail traces
        self.clusteredTraces["Pass"] = []
        self.clusteredTraces["Fail"] = []
        for t in self.listTraces:
            if t[1] == "Pass":
                self.clusteredTraces["Pass"].append(t[0])
            else:
                self.clusteredTraces["Fail"].append(t[0])
        #todo: cluster fail traces

    def printTrace(self):
        for trace in self.listTraces:
            s = ""
            for event in trace:
                s = s+event+" "
            print(s)

    def printClusteredTrace(self):
        for key, value in self.clusteredTraces.items():
            print(key)
            for trace in value:
                s = ""
                for event in trace:
                    s = s+event+" "
                print(s)
