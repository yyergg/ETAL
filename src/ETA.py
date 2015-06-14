import TraceGenerator
import TraceLoader
import RuleMiner
import RuleFilter
import RuleChecker
import WeightLearner
import os
import sys

TL = TraceLoader.TraceLoader()
TL.loadTrace("test/")
TL.clusterTraces()
TL.printClusteredTrace()
#sys.exit(0)

print("Pass Rules:")
RM = RuleMiner.RuleMiner()
RM.setTrace(TL.clusteredTraces["Pass"])
RM.setSupportThreshold(0.2)
RM.setConfidenceThreshold(0.2)
RM.miningRule()
# modify miningRule
RM.printRule(RM.rules,0)

for key, vlaue in TL.clusteredTraces.items():
    print(TL.clusteredTraces[key])
    RM2 = RuleMiner.RuleMiner()
    RM2.setTrace(TL.clusteredTraces[key])
    RM2.setSupportThreshold(0.6)
    RM2.setConfidenceThreshold(0.5)
    RM2.miningRule()
    # modify miningRule
    RM2.printRule(RM2.rules,0)

# First Level Filter
    print("Fail Rules after filter:")
    RuleFilter.getSubtract(RM2.rules, RM.rules)
    RM2.printRule(RM2.rules,0)

    failRuleset = []
    for r in RM2.getAllRules(RM2.rules):
        failRuleset.append(r)

# Second Level Filter
for key,value in TL.clusteredTraces.items():
    for rule in value:
        RuleChecker.ruleCheck(rule,value)

# Weight Learninig
WL = WeightLearner.WeightLearner(failRuleset,TL.clusteredTraces)

for key, vlaue in TL.clusteredTraces.items():
    WL.buildMatrix()
    WL.learn(key)

for key, vlaue in TL.clusteredTraces.items():
    TG = TraceGenerator.TraceGenerator(TL.clusteredTraces["Pass"] + TL.clusteredTraces[key])
    TG.buildGraph()

##for fr in failRuleset():
    print("generate trace for rule:",failRuleset[4])
    print("result:",TG.generateTrace(failRuleset[4]))


'''
example to test filter
R1 = RuleNode("a")
R2 = RuleNode("b")
R3 = RuleNode("c")
R7 = RuleNode("d")

R1.children.append(R2)
R1.children.append(R3)
R3.children.append(R7)

R4 = RuleNode("a")
R5 = RuleNode("b")
R6 = RuleNode("c")

R4.children.append(R5)
R4.children.append(R6)

RM.printRule(R1,0)
RM.printRule(R4,0)

RuleFilter.getSubtract(R1,R4)

RM.printRule(R1,0)
'''