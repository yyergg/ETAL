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

from abstraction import Abstraction
from Automata import Automata,State
from copy import deepcopy
import os
import json

class AutomataManager():
    def __init__(self,abstraction):
        self.automata = Automata(abstraction)

        self.abstraction = abstraction
        self.automata._Automata__setConsideredAttributes(self.abstraction.getConsideredAttributes())
        self.automata._Automata__setIgnoredAttributes(self.abstraction.getIgnoredAttributes())

    def newTrace(self):
        self.trace = []
        self.prevStateID = -1
        self.currentStateID = -1
        self.currentState = None
        self.edgeState = None

    def setParentPath(self,parentPath):
        self.parentPath = parentPath

    def getAutomata(self):
        return self.automata

    def getTrace(self):
        return self.trace

    def getCurrentState(self):
        return self.currentState

    def saveAutomata(self,automataDir):
        print("Save automata.")

        # clean the automata directory first
        for file in os.listdir(automataDir):
            targetFile = os.path.join(automataDir,file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)

        # dump states informations
        for state in self.automata.states:
            statePath = os.path.join(automataDir,"state"+str(state.ID)+".json")
            data = {'stateID':state.ID}
            data["stateType"] = state.Type
            data["stateXMLs"] = state.XMLs
            data["stateMoves"] = state.Moves
            with open(statePath, "w") as outfile:
                json.dump(data, outfile, indent=4)

        # dump edges informations
        edgePath = os.path.join(automataDir,"edges.json")
        edges = list(self.automata.edges)
        data = {'edges':edges}
        with open(edgePath, "w") as outfile:
                json.dump(data, outfile, indent=4)

    '''
    This function can load only one already existed automata as a current automata.
    '''
    def loadAutomata(self,automataDir,algo):
        for root,dirnames,filenames in os.walk(automataDir):
            for file in filenames:
                if file.startswith("state"):
                    stateFile = os.path.join(root,file)
                    state_json = open(stateFile)
                    stateData = json.load(state_json)
                    state_json.close()

                    # new a state
                    if stateData["stateType"] == "View":
                        # get first XML in stateXMLs
                        # ex: David-exp1\net.mandaria.tippytipper\version1\abstraction1\session9\traceSet\1\uidump0.xml
                        xml = self.getXMLbyStepID(stateData["stateXMLs"][0],algo)

                        newState = self.automata._Automata__generateState(xml)

                    if stateData["stateType"] == "Action":
                        # get first Move in stateMoves
                        # ex: David-exp1\net.mandaria.tippytipper\version1\abstraction1\session9\traceSet\1\move1.json
                        move = self.getMovebyStepID(stateData["stateMoves"][0],algo)

                        newState = self.automata._Automata__generateState(move)

                    newState.ID = stateData["stateID"]
                    newState.Type = stateData["stateType"]
                    newState.Moves = stateData["stateMoves"]
                    newState.XMLs = stateData["stateXMLs"]

                    # add new state into automata
                    self.automata.states.append(newState)

                    # update the stateNum of the automata
                    self.automata.stateNum += 1

                elif file.startswith("edges"):
                    edgeFile = os.path.join(root,file)
                    edge_json = open(edgeFile)
                    edgeData = json.load(edge_json)
                    edge_json.close()

                    self.automata.edges = edgeData["edges"]

        #return a duplicated automata
        return deepcopy(self.automata)

    '''
    This function can be called repeatedly, keep adding new state in current automata
    '''
    def loadSession(self,sessionDir):
        # sessionDir is 'David\\net.mandaria.tippytipper\\version1\\abstraction1\\session1\\traceSet'
        sessionNum = int( os.path.split(os.path.split(sessionDir)[0])[1].replace("session",""))
        abstractionNum = int( os.path.split(os.path.split(os.path.split(sessionDir)[0])[0])[1].replace("abstraction",""))
        versionNum = int( os.path.split(os.path.split(os.path.split(os.path.split(sessionDir)[0])[0])[0])[1].replace("version",""))

        for root,dirnames,filenames in os.walk(sessionDir):
            if dirnames != []:
                # each session enter once
                # dirnames = [1,10,2,3,4,5,6,7,8,9]
                # totalTrace = [1,2,3,4,5,6,7,8,9,10]
                totalTrace = sorted([int(x) for x in dirnames])
                for traceNum in totalTrace:
                    step = 0
                    while os.path.isfile(os.path.join(root,str(traceNum),"uidump"+str(step)+".xml")):
                        print("trace = ",str(traceNum),"step = ",str(step))
                        stepID = (versionNum,abstractionNum,sessionNum,int(traceNum),step)
                        xml = os.path.join(root,str(traceNum),"uidump"+str(step)+".xml")
                        if step == 0 : # handle the initial state in each session
                            self.updateAutomataByRestart(xml,stepID)
                        else:
                            move = os.path.join(root,str(traceNum),"move"+str(step)+".json")
                            action = self.automata._Automata__generateAction(move)
                            if action[0] == "restart":
                                self.updateAutomataByRestart(xml,stepID)
                            else:
                                self.updateAutomataByAction(action,stepID)
                                self.updateAutomataByXML(xml,stepID)
                        step += 1

    def getXMLbyStepID(self,stepID,algo):
        if algo == "SELabeler":
            versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID

            xml = os.path.join(self.parentPath,"version"+str(versionNum),"abstraction"+str(abstractionNum),\
                            "labeledTrace","traceSet",str(traceNum),"uidump"+str(stepNum)+".xml")
        else:
            versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
            xml = os.path.join(self.parentPath,"version"+str(versionNum),"abstraction"+str(abstractionNum),\
                            "session"+str(sessionNum),"traceSet",str(traceNum),"uidump"+str(stepNum)+".xml")
        return xml

    def getMovebyStepID(self,stepID,algo):
        if algo == "SELabeler":
            versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
            move = os.path.join(self.parentPath,"version"+str(versionNum),"abstraction"+str(abstractionNum),\
                            "labeledTrace","traceSet",str(traceNum),"move"+str(stepNum)+".json")
        else:
            versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
            move = os.path.join(self.parentPath,"version"+str(versionNum),"abstraction"+str(abstractionNum),\
                            "session"+str(sessionNum),"traceSet",str(traceNum),"move"+str(stepNum)+".json")
        return move

    def updateAutomataByRestart(self,xml,stepID,memInfo):
        self.edgeState = None
        self.currentState = self.automata._Automata__generateState(xml)
        tempViewList = self.currentState.viewList

        self.currentStateID = self.automata._Automata__addState(self.currentState,stepID) # view state
        for state in self.automata.states:
            if state.ID == self.currentStateID:
                self.currentState = state

        # 1. update current viewList
        self.currentState.viewList = tempViewList

        # 2. get memory information
        self.currentState.totalMemory = memInfo.pssTotal

        self.currentState.ID = self.currentStateID
        self.trace.append(self.currentState)

        return self.currentStateID


    def updateAutomataByXML(self,xml,stepID,memInfo):
        self.currentState = self.automata._Automata__generateState(xml)
        tempViewList = self.currentState.viewList

        if self.edgeState == None: # the beginning state
            self.currentStateID = self.automata._Automata__addState(self.currentState,stepID) # view state
            self.currentState.ID = self.currentStateID

            # get memory information
            self.currentState.totalMemory = memInfo.pssTotal

            self.trace.append(self.currentState)

        else: # the rest states, need to update edgeState's fromState and toState
            self.prevStateID = self.currentStateID
            self.currentStateID = self.automata._Automata__addState(self.currentState,stepID) # view state
            for state in self.automata.states:
                if state.ID == self.currentStateID:
                    self.currentState = state

            # 1. update current viewList
            self.currentState.viewList = tempViewList

            # 2. get memory information
            self.currentState.totalMemory = memInfo.pssTotal

            self.automata._Automata__addEdge(self.prevStateID,self.currentStateID)
            self.trace.append(self.currentState)

        return self.currentStateID

        #print("shortest path = "+str(self.automata.getShortestPath(self.automata.initialState.ID,self.currentState.ID)))

    def updateAutomataByAction(self,action,stepID):
        self.edgeState = State()
        self.edgeState.Type = "Action"
        self.edgeState.action = action
        self.prevStateID = self.currentStateID
        self.currentStateID = self.automata._Automata__addState(self.edgeState,stepID) # action state
        self.edgeState.ID = self.currentStateID
        print(" add edge prev = ",self.prevStateID," curr = ",self.currentStateID)
        self.automata._Automata__addEdge(self.prevStateID,self.currentStateID)
        self.trace.append(self.edgeState)

        return self.currentStateID















