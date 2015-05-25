import random
from DataStructure import Weight
import RuleChecker

class WeightLearner:
    def __init__(self, ruleset, clusteredTraces):
        self.maxWeightValue = 10
        self.populationSize = 200
        self.clusteredTraces = clusteredTraces
        self.ruleSet = ruleset
        self.listWeight = []
        for i in range(self.populationSize):
            newWeight = Weight()
            for j in range(len(self.ruleSet)):
                newWeight.weight.append(random.randint(0, self.maxWeightValue))
            newWeight.threshold = random.randint(0, self.maxWeightValue*len(self.ruleSet))
            newWeight.score = 0
            print(newWeight.weight,"|",newWeight.threshold,"|",newWeight.score)



