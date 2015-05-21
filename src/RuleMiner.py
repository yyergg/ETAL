from Rule import RuleNode


class RuleMiner:
    def __init__(self):
        self.__traces = []
        self.rules = None
        self.__allState = []
        self.__maxStateNumber = 0
        self.__maxDepth = 3
        self.__supportThreshold = 0.3
        self.__confidenceThreshold = 0.5        

    def printRule(self, root, level):
        if not root.removed:
            print("    "*level+root.eventName)
            for child in root.children:
                self.printRule(child, level+1)

    def setTrace(self, inputTraces):
        self.__traces = inputTraces

    def setTraceTest(self):
        trace = []
        trace = "0 0_3 1 1_7 2 2_0 1 1_1 3".split(" ")
        self.__traces.append(trace)
        trace = "0 0_3 1 1_7 3 3_0 1 1_1 3".split(" ")
        self.__traces.append(trace)

    def setSupportThreshold(self, value):
        self.__supportThreshold = value

    def setConfidenceThreshold(self, value):
        self.__confidenceThreshold = value

    def collectAllState(self):
        for t in self.__traces:
            for e in t:
                if (e.find("_") == -1 and not e in self.__allState):
                    self.__allState.append(e)
                    if int(e) > self.__maxStateNumber:
                        self.__maxStateNumber = int(e)

    def calculateSupport(self, statename):
        counter = 0.0
        for t in self.__traces:
            if statename in t:
                counter = counter + 1.0
        return counter/float(len(self.__traces))

    def extendRule(self, root, oldLabels, depth):
        #print("extending",root.eventName,oldLabels)
        possibleViews = {}
        possibleViewSupportCounter = {}
        for label in oldLabels:
            if len(self.__traces[label[0]]) > label[1] + 1:
                if self.__traces[label[0]][label[1] + 1] in possibleViews.keys():
                    possibleViews[self.__traces[label[0]][label[1] + 1]].append((label[0], label[1]+1))
                    possibleViewSupportCounter[self.__traces[label[0]][label[1] + 1]] += 1
                else:
                    possibleViews[self.__traces[label[0]][label[1] + 1]] = []
                    possibleViewSupportCounter[self.__traces[label[0]][label[1] + 1]] = 1
                    possibleViews[self.__traces[label[0]][label[1] + 1]].append((label[0], label[1]+1))

        for key, value in possibleViews.items():
            if float(possibleViewSupportCounter[key])/float(len(self.__traces)) > self.__supportThreshold:
                #print(key,float(possibleViewSupportCounter[key]),float(len(self.__traces)))
                newRule1 = RuleNode(key)
                postStateMatrix = []
                
                for v in value:
                    postStateArray = [0]*(self.__maxStateNumber+1)
                    i = v[1]
                    while i < len(self.__traces[v[0]]):
                        if self.__traces[v[0]][i].find("_") == -1:
                            postStateArray[int(self.__traces[v[0]][i])] = 1
                        i = i + 1
                    postStateMatrix.append(postStateArray)
                #print(postStateMatrix)
                i = 0
                while i < self.__maxStateNumber + 1:
                    j = 0
                    counter = 0.0
                    while j < len(value):
                        if postStateMatrix[j][i] == 1:
                            counter = counter + 1.0
                        j = j + 1

                    #print(key,str(i),counter,float(len(value)))

                    if (counter/float(len(value))) > self.__confidenceThreshold:
                        newLabels = []
                        j = 0
                        while j < len(value):
                            if postStateMatrix[j][i] == 1 and value[j][1] < len(self.__traces[value[j][0]]) - 1:
                                k = value[j][1] + 1
                                while k < len(self.__traces[value[j][0]]):
                                    if self.__traces[value[j][0]][k] == str(i):
                                        newLabels.append((value[j][0], k))
                                    k = k + 1
                            j = j + 1
                        newRule2 = RuleNode(str(i))
                        newRule1.children.append(newRule2)
                        #self.printRule(root, 0)
                        if depth < self.__maxDepth:
                            self.extendRule(newRule2, newLabels, depth+1)
                    i = i + 1
                if len(newRule1.children) != 0:
                    root.children.append(newRule1)
        #print("finish extending")

    def miningRule(self):
        self.rules = RuleNode("init")
        self.collectAllState()
        for state in self.__allState:
            if self.calculateSupport(state) >= self.__supportThreshold:
                labels = []
                i = 0
                while i < len(self.__traces):
                    j = 0
                    while j < len(self.__traces[i]):
                        if self.__traces[i][j] == state:
                            labels.append((i, j))
                        j = j + 1
                    i = i + 1
                newRule = RuleNode(state)
                self.extendRule(newRule, labels, 0)
                if len(newRule.children) > 0:
                    self.rules.children.append(newRule)
