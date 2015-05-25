import random
from DataStructure import Weight
import RuleChecker

class WeightLearner:
    def __init__(self, ruleset, clusteredTraces):
        self.maxWeightValue = 10
        self.populationSize = 200
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

    def printPopulation(self):
        for w in self.listWeight:
            print(w.weight,"|",w.threshold,"|",w.score)

    def calculateScore(self, target):
        for weight in self.listWeight:
            if weight.fresh:
                weight.fresh = False
                for key,value in self.clusteredTraces.items():
                    for trace in value:
                        sum = 0
                        i = 0
                        while i < len(self.ruleSet):
                            if RuleChecker.ruleCheck(self.ruleSet[i],trace):
                                sum += weight.weight[i]
                            i += 1
                        if sum >= weight.threshold:
                            if key == target:
                                weight.score += 1

    def eliminate(self):
        self.listWeight = sorted(self.listWeight, key = lambda x : x.score, reverse=True)