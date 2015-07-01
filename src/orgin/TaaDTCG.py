#-------------------------------------------------------------------------------
# Name:         TaaD test case generator
# Purpose:
#
# Author:      ASTROHSU
#
# Created:     24/06/2015
# Copyright:   (c) ASTROHSU 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from DataStructure import GraphNode
import sys
import os
import shutil
import json
import automataLoader
from TestCaseGenerator import TestCaseGenerator
import TestingTask

class TestCaseGenerator2(TestCaseGenerator):
    def __init__(self,task):
        rulefile = open("FailRule.txt")
        self.rulefile = rulefile
##        self.traces = traces
        self.ruleIndex = 0
        self.ruleStateIndex = 0
        self.shortestPathIndex = 0
        self.nodeMap = {}
        self.automataDir = "C:\\Users\\ASTROHSU\\Desktop\\Exp\\traces\\MN\\edu.nyu.cs.omnidroid.app\\version1\\abstraction1\\session16\\sessionAutomata"
        task.setParentPath("C:\\Users\\ASTROHSU\\Desktop\\Exp\\traces\\MN\\edu.nyu.cs.omnidroid.app")
        task.getAutomataByDir("C:\\Users\\ASTROHSU\\Desktop\\Exp\\sessionAutomata","TestCaseGenerator2")
        self.ruleInList = []
        self.shortestPath = []
        failStateList = []
        for line in rulefile.readlines():
            self.ruleInList.append(line.split())

    def getTestInput(self,task):
        print("-------------------------------")

        automata = task.getAutomata()
        state = task.getCurrentState()
        print("state =",state.ID)
        if self.shortestPathIndex >= len(self.shortestPath): # finish traverse shortest path
            print("finsh traverse shortest path")
            print("current rule ele = ",int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
            if state.ID == int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]): # back to traverse rule
                print("back to traverse rule")
                isSuccessor = False
                for id in automata.getSuccesorByID(int(self.ruleInList[self.ruleIndex][self.ruleStateIndex])):
                    if id == int(self.ruleInList[self.ruleIndex][self.ruleStateIndex+1]):
                        isSuccessor = True
                if isSuccessor:# idx+1 is an action of idx
                    print("the next rule is the successor")

                    ## get fucking action
                    stateFile = automataLoader.getStatePath(self.automataDir,int(self.ruleInList[self.ruleIndex][self.ruleStateIndex + 1]))
                    print("rule = ",self.ruleInList[self.ruleIndex])
                    print("rule idx = ",self.ruleIndex + 1)
                    print("rule ele = ",str(self.ruleInList[self.ruleIndex][self.ruleStateIndex + 1]))
                    print("stateFile = ",stateFile)
                    state_json = open(stateFile)
                    stateData = json.load(state_json)
                    state_json.close()
                    #print("state")
                    #print(stateData["stateMoves"][0])
                    move = self.getMovebyStepID(stateData["stateMoves"][0],self.automataDir)
                    move_json = open(move)
                    moveData = json.load(move_json)
                    move_Type = moveData["actionType"]
                    move_Argu = moveData["actionArgu"]
                    move_json.close()
                    self.ruleStateIndex += 2
                    return (move_Type,None,move_Argu)

                else:
                    print("the next rule is not the successor, find another shortest path")
                    print("Find path from ",int(self.ruleInList[self.ruleIndex][self.ruleStateIndex])," to",int(self.ruleInList[self.ruleIndex][self.ruleStateIndex+1]))
                    self.shortestPathIndex = 0
                    self.shortestPath = automata.getShortestPath(int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]), int(self.ruleInList[self.ruleIndex][self.ruleStateIndex+1]))
                    if len(self.shortestPath) == 0: # no path
                        print("no available path")
                        ## go fuck yourself
                        print("Bad rule, change to next rule")
                        self.ruleIndex += 1
                        self.ruleStateIndex = 0
                        return state.getTerminateKey()
                    else:
                        self.shortestPath.insert(0, int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
                        self.shortestPath.append(int(self.ruleInList[self.ruleIndex][self.ruleStateIndex+1]))
                        print("shortestpath = ",self.shortestPath)
            else:
                self.shortestPathIndex = 0
                self.shortestPath = automata.getShortestPath(state.ID, int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
                if len(self.shortestPath) == 0: # no path
                    print("no available path")
                    ## go fuck yourself
                    print("Bad rule, change to next rule")
                    self.ruleIndex += 1
                    self.ruleStateIndex = 0
                    return state.getTerminateKey()
                else:
                    self.shortestPath.insert(0, state.ID)
                    self.shortestPath.append(int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
                    print("shortestpath = ",self.shortestPath)
        elif state.ID != self.shortestPath[self.shortestPathIndex]: # keep traverse shortest path, however, missing on the path, find another path
            print("keep traverse shortest path, however, missing on the path")
            print("Find path from ",state.ID," to", self.ruleInList[self.ruleIndex][self.ruleStateIndex])
            self.shortestPathIndex = 0
            self.shortestPath = automata.getShortestPath(state.ID, int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
            if len(self.shortestPath) == 0: # no path
                ## go fuck yourself
                print("Bad rule, change to next rule")
                self.ruleIndex += 1
                self.ruleStateIndex = 0
                return state.getTerminateKey()
            else:
                self.shortestPath.insert(0, state.ID)
                self.shortestPath.append(int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
                print("shortestpath = ",self.shortestPath)
        # traverse shortest path
        print("traverse shortest path")

        ## get your fucking action
        print("shortestPath = ",self.shortestPath)
        print("shortestPathIndex = ",self.shortestPathIndex)
        action = self.shortestPath[self.shortestPathIndex+1]
        print("action = ",action)
        self.shortestPathIndex += 2
        return action

        print("-------------------------------")

    def getMovebyStepID(self,stepID,automataDir):
        versionNum,abstractionNum,sessionNum,traceNum,stepNum = stepID
        move = os.path.join(os.path.dirname(automataDir),"test",str(traceNum),"move"+str(stepNum)+".json")
        #print("move = ",move)
        return move


        '''
        if self.ruleStateIndex > len(self.ruleInList[self.ruleIndex]):
            self.ruleIndex += 1
            self.ruleStateIndex == 0
            print("rule finished")
            return state.getTerminateKey()

        elif state.ID != int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]):
            print(state.ID)
            self.shortestPath = automata.getShortestPath(state.ID,int(self.ruleInList[self.ruleIndex][self.ruleStateIndex]))
            #self.shortestPath = automata.getShortestPath(0,500)
            # if I can't traverse to initial node of rule, change rule
            if len(self.shortestPath) == 0:
                # check whether rule start state is a successor of the current state
                isSuccessor = False
                for successorID in automata.getSuccesorByID(state.ID):
                    if successorID == state.ID:
                        isSuccessor = True
                if isSuccessor:

                else:
                    self.ruleIndex += 1
                    self.ruleStateIndex == 0
                    print("Bad rule, change to next rule")
                    return state.getTerminateKey()
            else:
                self.shortestPathIndex += 2
                print("!!")
                print(self.shortestPath)
                targetMoveState = str(self.shortestPath[self.shortestPathIndex])
    ##            targetMoveState.ID =
                #get type & argu of the move
                move = getMovebyStepID(stateData["stateMoves"][0],automataDir)
                move_json = open(move)
                moveData = json.load(move_json)
                move_Type = moveData["actionType"]
                move_Argu = moveData["actionArgu"]
                move_json.close()
            return (move_Type,None,move_Argu)
        #
        else:
            self.ruleStateIndex += 1
        '''





