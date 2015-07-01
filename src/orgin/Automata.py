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
import random
import string
import os
import json
from copy import deepcopy

class View:
    def __init__(self,layer,viewIndex,xml=None):
        # xml is an etree element
        self.attrDict = {}
        self.layer = layer
        self.index = viewIndex
        self.buttonLineCoverage = 0

        # store each attribute as a dictionary key
        if xml != None:
            for attr in xml.attrib:
                self.attrDict[attr] = xml.attrib[attr]


    def isClickable(self):
        return self.attrDict["clickable"]

    def isScrollable(self):
        return self.attrDict["scrollable"]

    def isLayout(self):
        if "Layout" in self.attrDict["class"]:
            return True
        else: return False

    def getClass(self):
        return self.attrDict["class"]

    def getLayer(self):
        return self.layer

    def getIndex(self):
        return self.index

    def getCoverage(self):
        return self.buttonLineCoverage

    def getBounds(self):
        leftBound=int(self.attrDict["bounds"].replace("[","").split("]")[0].split(",")[0])
        topBound=int(self.attrDict["bounds"].replace("[","").split("]")[0].split(",")[1])
        rightBound=int(self.attrDict["bounds"].replace("[","").split("]")[1].split(",")[0])
        bottomBound=int(self.attrDict["bounds"].replace("[","").split("]")[1].split(",")[1])

        return (leftBound,topBound,rightBound,bottomBound)


class State():
    def __init__(self):
        self.ID = -1
        self.totalMemory = -1
        self.Type = "View"
        self.viewList = []
        self.XMLs = []
        self.Moves = []
        self.action = None

    def getLegalActions(self):
        # Possible actions are ("click",view,(x1,y1)),("text",view,"a random string"),("roll",view,(dx,dy))
        # and ("keyevent",None,(a random system key,"it's meaning"))

        self.legalActions = []
        self.legalActions.extend(self.getClickableViews())
##        self.legalActions.extend(self.getEditTextViews())
        # roll is removed temporarily
        #self.legalActions.extend(self.getScrollableViews())
        if random.randint(0,3) < 1: # only 25% to add system key in legal actions
            self.legalActions.append(self.getSystemKey())
        return self.legalActions

    def getClickableViews(self):
        # action is ("click",view,(x1,y1))
        self.clickableViews = []
        for view in self.viewList:
            if view.attrDict["clickable"] == "true":
                left = view.getBounds()[0]
                top = view.getBounds()[1]
                right = view.getBounds()[2]
                bottom = view.getBounds()[3]
                self.clickableViews.append(["click",view,[int(left+right)/2,int(top+bottom)/2]])
        return self.clickableViews

    def getEditTextViews(self,text = None):
        # action is ("text",view,"a random string")
        self.editTextViews = []
        if text == None:
            text = self.getRandText()
        for view in self.viewList:
            if view.attrDict["class"] == "android.widget.EditText":
                self.editTextViews.append(["text",view,text])
        return self.editTextViews

    def getScrollableViews(self):
        # action is ("roll",view,(dx,dy))
        self.scrollableViews = []
        for view in self.viewList:
            if view.attrDict["scrollable"] == "true":
                self.scrollableViews.append(["roll",view,[random.randint(-20,20),random.randint(-20,20)]])
        return self.scrollableViews

    def getSystemKey(self,key=None):
        # action is ("keyevent",None,(a random system key,"it's meaning"))
        self.keyEvents = [('4',"BACK")]
        if key == None:
            keyEvent = random.choice(self.keyEvents)
        else:
            for Key in self.keyEvents:
                if key == Key[0] or key == int(Key[0]):
                    keyEvent = Key

        self.systemKey = ["keyevent",None,keyEvent]

        return self.systemKey

    def getTerminateKey(self):
        # action is ("terminate",None,"")
        return ("terminate",None,"")

    def getRestartKey(self):
        # action is ("restart",None,"")
        return ("restart",None,"")

    def getRandText(self,length = None):
        if length == None:
            size = random.randint(0,20)
        else:
            size = length
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for i in range(size))

class Automata():
    def __init__(self,abstraction):
        self.initialState = None
        self.states = []
        self.edges = []
        self.stateNum = 0
        self.abstraction = abstraction
        self.consideredAttributes = []
        self.ignoredAttributes = []

    def getStateByID(self,id):
        # return a state whose ID is id
        for state in self.states:
            if state.ID == id:
                return state

    def getPredecessorByID(self,id):
        # returns like [2,4,6]
        returnList = []
##        actionNodes = []
        for fromID,toID in self.edges:
            if toID == id:
                returnList.append(fromID)

        return returnList

    def getSuccesorByID(self,id):
        # returns like [2,4,6]
        returnList = []
##        actionNodes = []
        for fromID,toID in self.edges:
            if fromID == id:
                returnList.append(toID)

##
##        for action in actionNodes:
##            for fromID,toID in self.edges:
##                print(fromID,toID,action.ID)
##                if fromID == action.ID:
##                    print(str(toID,(action.actionType,action.targetView,action.actionArguments)))
##                    returnList.append((toID,()))
##
##        print("return in getSucc = ",str(returnList))
        return returnList


    def getShortestPath(self,fromID,toID):
        '''
        Reference to Dijkstra Algorithm on wikipedia
        '''
        print("Shortest path from state id = ",str(fromID),"to state id = ",str(toID))
        if fromID == toID :
            return []

        def Extract_Min(Q,Dist):
            minDist = float("inf")
            minState = None
            for state in Q:
                #print("state id in extract min ",state.ID)
                if minDist > Dist[state.ID]:
                    minDist = Dist[state.ID]
                    minState = state
            if minState == None: # can't find a min state
                return -1
            Q.remove(minState)
            return minState.ID

        # initialize
        Dist = {}
        Prev ={}
        for state in self.states:
            Dist[state.ID] = float('inf')
            Prev[state.ID] = None

        Dist[fromID] = 0
        S = []

        # initial Q
        Q = []
        for state in self.states:
            if state.Type == "View":
                Q.append(state)

        # u and v are all just ID, not states
        while len(Q) != 0:
            u = Extract_Min(Q,Dist)
##            if u == toID: # no need to keep traversing the nodes larger than toID
##                print(" u == toID = ",u)
##                break
            if u == -1: # end of traversing
                break
            S.append(u)
            for a in self.getSuccesorByID(u): # get all succ actions
                for v in self.getSuccesorByID(a): # get all succ views
##                    print("u = ",str(u)," a =",str(a)," v = ",str(v))
                    if Dist[v] > Dist[u] + 2: # 2 is the distance from u to v
                        actionState = self.getStateByID(a)
                        Dist[v] = Dist[u] + 2
                        Prev[v] = (u,actionState.action)

        # get return action list from fromID to toID
        returnList = []
        u = toID
        # Prev[u] looks like (4,("click",view,(250,250)))
        while Prev[u] != None:
##            print("Prev [u] = ",Prev[u])
            returnList.insert(0,Prev[u][1])
            u = Prev[u][0]
        print("shortest path = "+str(returnList))
        return returnList


    def findShortestPath(self, src, dst):
        print("find shortest path",src,dst)
        for key,value in self.nodeMap.items():
            value.BFSParent = None
        visited = []
        visited.append(src)
        frontier = []
        frontier.append(self.nodeMap[src])
        counter = 0
        while counter < len(self.nodeMap):
            nextFrontier = []
            for i in frontier:
                for child in i.children:
                    #print(i.name,"->",child.name)
                    if child.name not in visited:
                        visited.append(child.name)
                        child.BFSParent = i
                        if child.name == dst:
                            return self.traverseBack(child)
                        else:
                            nextFrontier.append(child)
            frontier = nextFrontier
            counter += 1
##
    def traverseBack(self,dst):
        result = []
        while dst.BFSParent != None:
            print(dst.BFSParent.name)
            result.append(dst.name)
            dst = dst.BFSParent
        result.append(dst.name)
        result.reverse()
        result = result[:-1]
        return result


    def getViews(self,root,layer):
        returnList = []
        for child in root:
          returnList.append((child,layer))
          returnList.extend(self.getViews(child,layer+1))
        return returnList

    def compareState(self,state1,state2):
##        print("compare: ",state1.Type,state2.Type)
        if state1.Type != state2.Type:
##            print("different type")
            return False

        # compare two views
        if state1.Type == "View" and state2.Type == "View":
##            print("compare two view")
            viewList1 = deepcopy(state1.viewList)
            viewList2 = deepcopy(state2.viewList)
            if self.abstraction.compare(viewList1,viewList2) == True:
                return True
            else:
                return False
##            if len(state1.viewList) != len(state2.viewList):
##                print("different length of viewList")
##                return False
##
##            else:
##                for (view1,view2) in zip(state1.viewList,state2.viewList):
##                    if self.__compareView(view1,view2) == False:
##                        print("compare view false")
##                        return False
##                return True

        # compare two actions
        if state1.Type == "Action" and state2.Type == "Action":
            # action is ("click",view,(250,250))
##            print("compare two action")
            if state1.action[0] != state2.action[0]:
                return False
            elif state1.action[2] != state2.action[2]:
                return False
            else :
##                if state1.action[1] == None and state2.action[1] == None:
##                    print("both views are None")
##                    return True
##
##                elif state1.action[1] == None or state2.action[1] == None:
##                    print("A view is None")
##                    return False

                if self.compareView(state1.action[1],state2.action[1]):
                    return True
                else:
                    return False

##                # should be improved
##                viewList1 = [deepcopy(state1.targetView)]
##                viewList2 = [deepcopy(state2.targetView)]
##                if self.abstraction.compare(viewList1,viewList2) == True:
##                    return True
##                else:
##                    return False

    def compareView(self,view1,view2):
        if view1 == None and view2 == None or view1 == 'None' and view2 == 'None':
            #print("both views are None")
            return True

        elif view1 == None or view2 == None or view1 == 'None' or view2 == 'None':
            #print("A view is None")
            return False

        elif len(view1.attrDict) != len(view2.attrDict):
            #print("different attributes amounts")
            return False

        elif len(self.consideredAttributes) != 0:
            for attr in self.consideredAttributes:
                #print("considered "+view1.attrDict[attr] +" "+ view2.attrDict[attr])
                if view1.attrDict[attr] != view2.attrDict[attr]: # any attr is different then return False
                    return False
            return True

        elif len(self.ignoredAttributes) != 0:
            for attr in view1.attrDict: # get all possible attributes
                if attr not in self.ignoredAttributes:
                    #print("ignored "+view1.attrDict[attr] +" "+ view2.attrDict[attr])
                    if view1.attrDict[attr] != view2.attrDict[attr]: # any attr is different then return False
                        return False
            return True

    def display(self):
        print("")
        print("-----------------Start printing automata.--------------",end="")
        for state in self.states:
            print("")
            print("State     ID = ",state.ID)
            print("State   type = ",state.Type)
            print("State   XMLs = ",state.XMLs)
            print("State  Moves = ",state.Moves)
            print("State action = ",state.action)
            print("State contains ",len(state.viewList)," views.")
        print("\nEdges = ",self.edges)
        print("---------------------End of printing.------------------")
        print("")

##        try:
##            from graphviz import Digraph
##        except ImportError:
##            print("require module 'graphviz'")
##
##        dot = Digraph()
##        for state in self.states:
##            if state.Type == "View":
##                dot.attr('node', shape='box')
##            else:
##                dot.attr('node', shape='ellipse')
##            dot.node(str(state.ID))
##        for edge in self.edges:
##            dot.edge(str(edge[0]), str(edge[1]))
##        OutputMakeup(dot, True, None,None,None)

##        import matplotlib
##        matplotlib.rcParams["savefig.dpi"]


    def __setConsideredAttributes(self,attrList):
        self.consideredAttributes = attrList

    def __setIgnoredAttributes(self,attrList):
        self.ignoredAttributes = attrList

    def __generateState(self,Path):
        # Path can be xml file or move file
        if Path.endswith("xml"):
            import xml.etree.ElementTree as ET
            xml = ET.parse(Path)
            root = xml.getroot()
            viewList = self.getViews(root,1)

            state = State()

            for index,view in enumerate(viewList):
                # View(layer,index,xml)
                newView = View(view[1],index,view[0])
                state.viewList.append(newView)

        elif Path.endswith("json"):
            move_json = open(Path)
            moveData = json.load(move_json)
            move_json.close()

            state = State()
            layer = moveData["layer"]
            index = moveData["index"]

            # View(layer,index,None)
            targetView = View(layer,index)

            xml = moveData["targetViewAttributes"]
            if xml == "None":
                targetView = "None"
            else:
                for attr in xml:
                    targetView.attrDict[attr] = xml[attr]
            state.action = [moveData["actionType"],targetView,moveData["actionArgu"]]

        return state

    def __generateAction(self,Path):
        if Path.endswith("json"):
            move_json = open(Path)
            moveData = json.load(move_json)
            move_json.close()

            layer = moveData["layer"]
            index = moveData["index"]

            # View(layer,index,None)
            targetView = View(layer,index)

            xml = moveData["targetViewAttributes"]
            if xml == "None":
                targetView = "None"
            else:
                for attr in xml:
                    targetView.attrDict[attr] = xml[attr]

            return [moveData["actionType"],targetView,moveData["actionArgu"]]

    def __addState(self,newState,stepID):
        #print("addState",end=" ")
        if newState.Type == "View":# record which trace which xml file
            if stepID not in newState.XMLs:
                newState.XMLs.append(stepID)
        if newState.Type == "Action":# record which trace which move file
            #print("action added = ",newState.actionType,newState.targetView,newState.actionArguments)
            if stepID not in newState.Moves:
                newState.Moves.append(stepID)

        if len(self.states) == 0: # the first time can add a new state directly
            self.initialState = newState
            self.initialState.ID = 0
        else:
            for state in self.states:
                if self.compareState(state,newState) == True:
                    if newState.Type == "View":
                        if stepID not in state.XMLs:
                            state.XMLs.append(stepID)
                    if newState.Type == "Action":
                        if stepID not in state.Moves:
                            state.Moves.append(stepID)
                    #print("same state")
                    return state.ID
##        print("type = ",newState.Type)
        # TODO why a None targetView can add a new state
        newState.ID = self.stateNum
        self.stateNum += 1
        self.states.append(newState)
##        print("states number = ",len(self.states))
##        for state in self.states:
##            print("state id = ",state.ID," type = ",state.Type)
        return newState.ID

    def __addEdge(self,id1,id2):
        if [id1,id2] not in self.edges:
            self.edges.append([id1,id2])












