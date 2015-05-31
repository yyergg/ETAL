import os
import sys
import re

class TraceLoader:
    def __init__(self):
        self.listTraces = []
        self.clusteredTraces = {}
        self.pathTraceFolder = ""

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
                i = 0
                while i < len(lines):
                    if lines[i].find("CLICK") != -1:
                        if preState == "":
                            print("Error: Click before any state. In", os.path.join(root,filename))
                        newTrace.append(preState+"_"+regexClick.search(lines[i]).group(0))
                    elif lines[i].find("state_") != -1:
                        preState = regexState.search(lines[i]).group(0)
                        newTrace.append(preState)
                    elif lines[i].find("error free") != -1:
                        self.listTraces.append((newTrace, "Pass"))
                        break
                    else:
                        tag = self.findFailTag(lines[i:])
                        #print(filename,tag)
                        self.listTraces.append((newTrace, tag))
                        break
                    i += 1


    def findFailTag(self, lines):
        i = 0
        stackHead = ""
        userHead = ""
        while i < len(lines):
            if lines[i].startswith("E/AndroidRuntime") and lines[i].find("at ")!=-1:
                stackMember = lines[i][lines[i].find("at ")+2:].strip()
                if stackHead == "":
                    stackHead = stackMember
                if not (stackMember.startswith("android")
                    or stackMember.startswith("java")
                    or stackMember.startswith("com.android")
                    or stackMember.startswith("dalvik")):
                    userHead = stackMember
            i += 1
        return stackHead+" called by "+userHead


    def clusterTraces(self):
        for t in self.listTraces:
            if t[1] not in self.clusteredTraces:
                self.clusteredTraces[t[1]] = []
            self.clusteredTraces[t[1]].append(t[0])

    def printTrace(self):
        for trace in self.listTraces:
            print(" ".join(trace[0]) + " " + trace[1])

    def printClusteredTrace(self):
        for key, value in self.clusteredTraces.items():
            print(key)
            for trace in value:
                s = ""
                for event in trace:
                    s = s+event+" "
                print(s)
