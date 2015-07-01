from DataStructure import RuleNode


class RuleMiner:
    def __init__(self):
        self.traces = []
        self.rules = None
        self.allState = []
        self.maxStateNumber = 0
        self.maxDepth = 5
        self.supportThreshold = 0.3
        self.confidenceThreshold = 0.5
        self.returRule = []

    def printRule(self, root, level):
        if not root.removed:
            print("    "*level+root.eventName)
            for child in root.children:
                self.printRule(child, level+1)

    def setTrace(self, inputTraces):
        self.traces = inputTraces

    def setTraceTest(self):
        trace = []
        trace = "0 0_3 1 1_7 2 2_0 1 1_1 3".split(" ")
        self.traces.append(trace)
        trace = "0 0_3 1 1_7 3 3_0 1 1_1 3".split(" ")
        self.traces.append(trace)

    def setSupportThreshold(self, value):
        self.supportThreshold = value

    def setConfidenceThreshold(self, value):
        self.confidenceThreshold = value

    def collectAllState(self):
        for trace in self.traces:
            i = 0
            for state in trace:
                if ((i%2) == 0 and not state in self.allState):
                    self.allState.append(state)
                    if int(state) > self.maxStateNumber:
                        self.maxStateNumber = int(state)
                i += 1

    def calculateSupport(self, statename):
        counter = 0.0
        for t in self.traces:
            if statename in t:
                counter = counter + 1.0
        return counter/float(len(self.traces))

    def extendRule(self, root, oldLabels, depth):
        #print("extending",root.eventName,oldLabels)
        possibleViews = {}
        possibleViewSupportCounter = {}
        for label in oldLabels:
            if len(self.traces[label[0]]) > label[1] + 1:
                if self.traces[label[0]][label[1] + 1] in possibleViews.keys():
                    possibleViews[self.traces[label[0]][label[1] + 1]].append((label[0], label[1]+1))
                    possibleViewSupportCounter[self.traces[label[0]][label[1] + 1]] += 1
                else:
                    possibleViews[self.traces[label[0]][label[1] + 1]] = []
                    possibleViewSupportCounter[self.traces[label[0]][label[1] + 1]] = 1
                    possibleViews[self.traces[label[0]][label[1] + 1]].append((label[0], label[1]+1))

        for key, value in possibleViews.items():
            if float(possibleViewSupportCounter[key])/float(len(self.traces)) > self.supportThreshold:
                #print(key,float(possibleViewSupportCounter[key]),float(len(self.traces)))
                newRule1 = RuleNode(key)
                postStateMatrix = []

                for v in value:
                    postStateArray = [0]*(self.maxStateNumber+1)
                    i = v[1]
                    while i < len(self.traces[v[0]]):
                        #if self.traces[v[0]][i].find("_") == -1:
                        if i%2 == 0:
                            postStateArray[int(self.traces[v[0]][i])] = 1
                        i = i + 1
                    postStateMatrix.append(postStateArray)
                #print(postStateMatrix)
                i = 0
                while i < self.maxStateNumber + 1:
                    j = 0
                    counter = 0.0
                    while j < len(value):
                        if postStateMatrix[j][i] == 1:
                            counter = counter + 1.0
                        j = j + 1
                    #print(key,str(i),counter,float(len(value)))
                    if (counter/float(len(value))) > self.confidenceThreshold:
                        newLabels = []
                        j = 0
                        while j < len(value):
                            if postStateMatrix[j][i] == 1 and value[j][1] < len(self.traces[value[j][0]]) - 1:
                                k = value[j][1] + 1
                                while k < len(self.traces[value[j][0]]):
                                    if self.traces[value[j][0]][k] == str(i):
                                        newLabels.append((value[j][0], k))
                                    k = k + 1
                            j = j + 1
                        newRule2 = RuleNode(str(i))
                        newRule1.children.append(newRule2)
                        #self.printRule(root, 0)
                        if depth < self.maxDepth:
                            self.extendRule(newRule2, newLabels, depth+1)
                    i = i + 1
                if len(newRule1.children) != 0:
                    root.children.append(newRule1)
        #print("finish extending")

    def miningRule(self):
        self.rules = RuleNode("init")
        self.collectAllState()
        for state in self.allState:
            if self.calculateSupport(state) >= self.supportThreshold:
                labels = []
                i = 0
                while i < len(self.traces):
                    j = 0
                    while j < len(self.traces[i]):
                        if self.traces[i][j] == state:
                            labels.append((i, j))
                        j = j + 1
                    i = i + 1
                newRule = RuleNode(state)
                self.extendRule(newRule, labels, 0)
                if len(newRule.children) > 0:
                    self.rules.children.append(newRule)

    def getAllRules(self, root):
        self.returRule.append(root.eventName)
        if len(root.children) == 0:
            yield self.returRule[1:]
            del self.returRule[-1]
        else:
            for c in root.children:
                yield from self.getAllRules(c)
            del self.returRule[-1]

