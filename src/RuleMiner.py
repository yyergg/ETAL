import Rule.RuleNode

class RuleMiner:
    __traces = []
    __rules = None
    __allState = []
    __supportThreshold = 0.15
    __confidenceThreshold = 0.5

    def setTrace(self, inputTraces):
        self.__traces = inputTraces

    def setSupportThreshold(self, value):
        self.__supportThreshold = value

    def setConfidenceThreshold(self, value):
        self.__confidenceThreshold = value

    def collectAllState(self):
        for t in self.__traces:
            for e in t:
                if e.find("_") == -1 and not e in self.__allState:
                    self.__allState.append(e)

    def calculateSupport(self, statename):
        counter = 0.0
        for t in self.__traces:
            if statename in t:
                counter = counter + 1.0
        return counter/float(len(self.__traces))

    def extendRule(self, root, preLabels):
        possibleViews = {}
        for label in preLabels:
            if len(self.__traces[label[0]]) > label[1] + 1:
                if self.__traces[label[0]][label[1] + 1] in possibleViews:
                    possibleViews[self.__traces[label[0]][label[1] + 1]].append((label[0],label[1]+1))
                else:
                    possibleViews[self.__traces[label[0]][label[1] + 1]] = []
                    possibleViews[self.__traces[label[0]][label[1] + 1]].append((label[0],label[1]+1))

        #for key, value in possibleViews:
        #    currentLabel

    def miningRule(self):
        root = RuleNode("init")
        self.collectAllState()
        for state in self.__allState:
            if self.calculateSupport(state) >= self.__supportThreshold:
                labels = []
                i = 0
                j = 0
                while i < len(self.__traces):
                    while j < len(self.__traces[i]):
                        if self.__traces[i][j] == state:
                            labels.append((i,j))
                newRule = RuleNode(state)
                self.extendRule(newRule,labels)
                if len(newRule.children) > 0:
                    root.children.append(newRule)
