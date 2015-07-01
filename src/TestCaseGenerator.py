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

import random
from copy import deepcopy

class TestCaseGenerator:
    def getTestInput(self,task):
        pass

class Monkey(TestCaseGenerator):
    def __init__(self):
        pass

    def getTestInput(self,task):
        state = task.getCurrentState()
        actions = state.getLegalActions()

        if len(actions) == 0:
            return state.getSystemKey()
        else:
            return random.choice(actions)

class DFS(TestCaseGenerator):
    def __init__(self):
        self.mode = "newState"
        self.previousID = -1
        self.currentID = -1
        self.previousAction = None
        self.historyPath = []
        self.counter = 0

        # historyDict = {ID:[clickedCoord,historyPath,isTraveled,parentID],...}
        self.historyDict = {}

    def getTestInput(self,task):
        self.previousID = self.currentID
        self.state = task.getCurrentState()
        self.currentID = self.state.ID

        self.mode = self.checkMode(self.currentID)
        print("!!!!!!!!mode = ",self.mode,"!!!!!!!!!")

        if self.mode == "newState":
            action = self.newStateAction()

        elif self.mode == "sameState":
            action = self.sameStateAction()

        elif self.mode == "backToParent":
            action = self.backToParentAction()

        elif self.mode == "backToNormal":
            action = self.backToNormalAction()

        self.historyPath.append(action)
        self.printInfo()
        return action


    def newStateAction(self):
        actions = self.state.getClickableViews()

        # There is at least one action can do.
        if len(actions) != 0:
            # pick the first action
            action = actions[0]

            # initial historyDict with new state ID
            if self.currentID == 0:
                self.historyDict[self.currentID] = [[action[2]],[self.state.getRestartKey()],False,self.previousID]
            else:
                self.historyDict[self.currentID] = [[action[2]],deepcopy(self.historyPath),False,self.previousID]

            print("new state, new action")
            self.parentID = self.previousID
            self.normalID = self.currentID
            return action

        # There is no any action can do in a new state.
        else:
            action = self.state.getSystemKey(4)

            # initial historyDict with new state ID
            self.historyDict[self.currentID] = [[],deepcopy(self.historyPath),True,self.previousID]

            print("new state, no action")
            self.mode = "backToParent"
            self.counter = 0
            self.parentID = self.previousID
            self.normalID = self.currentID

            return action

    def sameStateAction(self):
        actions = self.state.getClickableViews()

        # find an action to do and update clickedCoord
        for action in actions:
            clickPoint = action[2]
            if clickPoint not in self.historyDict[self.currentID][0]:
                self.historyDict[self.currentID][0].append(clickPoint)
                print("same state, pick an action")
                return action

        # don't have any new move can do, update isTraveled and back to parent
        action = self.state.getSystemKey(4)
        self.historyDict[self.currentID][2] = True

        if self.historyDict[self.currentID][3] == -1:
            print("same state, initial state traveled, terminate.")
            return self.state.getTerminateKey()
        else:
            print("same state, no action, back to parent")
            self.mode = "backToParent"
            self.counter = 0
            self.parentID = self.historyDict[self.currentID][3]

            return action

    def backToParentAction(self):
        path = self.historyDict[self.parentID][1]
        if self.counter > len(path):
            print("can't back to parent, terminate.")
            return self.state.getTerminateKey()
        else:
            action = path[self.counter]
            self.counter += 1

            print("back to parent")
            return action

    def backToNormalAction(self):
        # try to use simple "back" button to back to normal
        if self.counter == -1:
            if self.currentID == 0: # initial state
                pass
            else:
                self.counter += 1
                print("back to normal")
                return self.state.getSystemKey(4)

        path = self.historyDict[self.normalID][1]
        if self.counter > len(path):
            print("can't back to normal, terminate.")
            return self.state.getTerminateKey()
        else:
            action = path[self.counter]
            self.counter += 1
            print("back to normal")
            return action

    def checkMode(self,id):
        if self.mode == "backToParent":
            if id == self.parentID:
                return "sameState"
            else:
                return "backToParent"

        elif self.mode == "backToNormal":
            if id == self.normalID:
                return "sameState"
            else:
                return "backToNormal"

        elif id == self.previousID:
            return "sameState"

        elif self.isVisited(self.currentID):
            self.counter = -1
            return "backToNormal"

        else:
            return "newState"

    def isVisited(self,id):
        if id in self.historyDict:
            return True

        else: return False

    def printInfo(self):
        print("")
        print("--------------------------------history information--------------------------------")
        for id in self.historyDict:
            print("id = ",id," value = ",self.historyDict[id])
            print("")
        print("-----------------------------------------------------------------------------------")
        print("")












