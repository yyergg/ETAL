import os
import sys
import re

class TraceLoader:
    def __init__(self):
        self.listTraces = []
        self.clusteredTraces = {}
        self.pathTraceFolder = ""

    def loadTrace(self,pathTraceFolder):

        self.pathTraceFolder = os.path.join(os.getcwd(),"..",pathTraceFolder)
        listTraces = []
        print(self.pathTraceFolder)
        for root, dirs, files in os.walk(self.pathTraceFolder):
            for filename in files:
                if filename == "trace.txt":
                    infile = open(os.path.join(root,filename), 'r')
                    lines = infile.readlines()
                    infile.close()

                    newTrace = []
                    preState = ""
                    i = 0
                    while i < len(lines):
                        #print("line = ",lines[i])
                        if lines[i].find("move") != -1:
                            if preState == "":
                                print("Error: Click before any state. In", os.path.join(root,filename))
                            #click = preState+"_"+lines[i].split(" => ")[1].replace("click ","").replace("\n","")
                            click = lines[i].split(" => ")[1].replace("state","").replace("\n","")
                            #print("click="+click)
                            newTrace.append(click)
                        elif lines[i].find("uidump") != -1:
                            preState = lines[i].split(" => ")[1].replace("state","").replace("\n","")
                            newTrace.append(preState)
                            #print("state="+preState)
                        elif lines[i].find("pass") != -1:
                            self.listTraces.append((newTrace, "Pass"))
                            break
                        elif lines[i].find("fail") != -1:
                            tag = self.findFailTag(lines[i:])
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
        if stackHead == "" and userHead == "":
            return "No call stack"
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
        #print(value)