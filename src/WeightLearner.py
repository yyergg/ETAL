import random
from DataStructure import Weight
import RuleChecker

class WeightLearner:
    def __init__(self, ruleset, clusteredTraces):
        self.RuleTraceMatrix = {}
        self.maxWeightValue = 10
        self.populationSize = 200
        self.learningRound = 100
        self.killRate = 0.5
        self.clusteredTraces = clusteredTraces
        self.ruleSet = ruleset
        self.listWeight = []
        for i in range(self.populationSize):
            newWeight = Weight()
            for j in range(len(self.ruleSet)):
                newWeight.weight.append(random.randint(0, self.maxWeightValue))
            newWeight.threshold = random.randint(0, self.maxWeightValue*len(self.ruleSet))
            newWeight.score = 0
            newWeight.fresh = True
            self.listWeight.append(newWeight)


    def getTopRule(self):
        maxWeightRuleIndex = 0
        maxWeight = 0
        i = 0
        while i < len(self.listWeight[0].weight):
            if self.listWeight[0].weight[i] > maxWeight:
                maxWeight = self.listWeight[0].weight[i]
                maxWeightRuleIndex = i
            i += 1
        return self.ruleSet[maxWeightRuleIndex]


    def learn(self,target):
##        self.printPopulation()
        i = 0
        while i < self.learningRound:
            print("-------------Round",i,"-----------------")
            self.calculateScore(target)
            self.eliminate()
            self.crossover()
##            self.printPopulation()
            i += 1
        self.eliminate()

##    def printPopulation(self):
##        for w in self.listWeight:
##            print(w.weight,"|",w.threshold,"|",w.score)

    def buildMatrix(self):
        for key,value in self.clusteredTraces.items():
            self.RuleTraceMatrix[key] = []
            for trace in value:
                vector = []
                for rule in self.ruleSet:
                    vector.append(RuleChecker.ruleCheck(rule,trace))
                self.RuleTraceMatrix[key].append(vector)

    def calculateScore(self, target):
        for weight in self.listWeight:
            if weight.fresh:
                weight.fresh = False
                for key,value in self.clusteredTraces.items():
                    i=0
                    while i < len(value):
                        sum = 0
                        j = 0
                        while j < len(self.ruleSet):
                            if self.RuleTraceMatrix[key][i][j]:
                                sum += weight.weight[j]
                            j += 1
                        if sum >= weight.threshold:
                            if key == target:
                                weight.score += 1
                        else:
                            if key != target:
                                weight.score += 1
                        i += 1

    def eliminate(self):
        self.listWeight = sorted(self.listWeight, key = lambda x : x.score)
        self.listWeight = self.listWeight[int(self.populationSize*self.killRate):]

    def crossover(self):
        while len(self.listWeight) < self.populationSize:
            newWeight = Weight()
            parent1 = self.listWeight[random.randint(0,len(self.listWeight)-1)]
            parent2 = self.listWeight[random.randint(0,len(self.listWeight)-1)]
            cutpoint = random.randint(0,len(self.ruleSet))
            newWeight.weight = parent1.weight[:cutpoint] + parent2.weight[cutpoint:]
            newWeight.threshold = random.randint(min(parent1.threshold,parent2.threshold),
                max(parent1.threshold,parent2.threshold))
            newWeight.score = 0
            newWeight.fresh = True
            self.listWeight.append(newWeight)