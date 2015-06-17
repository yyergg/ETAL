import TraceGenerator
import TraceLoader
import RuleMiner
import RuleFilter
import RuleChecker
import WeightLearner
import os
import sys

TL = TraceLoader.TraceLoader()
TL.loadTrace("test")
TL.clusterTraces()
TL.printClusteredTrace()
#sys.exit(0)

print("Pass Rules:")
RM = RuleMiner.RuleMiner()
RM.setTrace(TL.clusteredTraces["Pass"])
RM.setSupportThreshold(0.5)
RM.setConfidenceThreshold(0.5)
RM.miningRule()
RM.printRule(RM.rules,0)


failRuleset = []
for key, vlaue in TL.clusteredTraces.items():
    print(TL.clusteredTraces[key])
    RM2 = RuleMiner.RuleMiner()
    RM2.setTrace(TL.clusteredTraces[key])
    RM2.setSupportThreshold(0.6)
    RM2.setConfidenceThreshold(0.5)
    RM2.miningRule()
    RM2.printRule(RM2.rules,0)
    # First Level Filter XOR - Remove pass rule which existing in fail rule from fail rule set
    RuleFilter.getSubtract(RM2.rules, RM.rules)
    print("Fail Rules after filter:")    
    RM2.printRule(RM2.rules,0)
    for r in RM2.getAllRules(RM2.rules):
        failRuleset.append(r)

# Second Level Filter - Put fail rule into pass traces
i = 0
while i < len(failRuleset):
    if len(failRuleset[i]) == 0:
        print("del", i)
        del failRuleset[i]
        continue
    counter = 0
    for t in TL.clusteredTraces["Pass"]:
        if RuleChecker.ruleCheck(failRuleset[i],t):
            counter += 1
    if counter > 2:
        del failRuleset[i]
        i -= 1
    i += 1

print(failRuleset)

# Weight Learninig
WL = WeightLearner.WeightLearner(failRuleset,TL.clusteredTraces)
WL.buildMatrix()

for key, vlaue in TL.clusteredTraces.items():
    WL.learn(key)

traceInList = []
for key, value in TL.clusteredTraces.items():
    traceInList = traceInList + value

    
TG = TraceGenerator.TraceGenerator(traceInList)
TG.buildGraph()

for fr in failRuleset:
    print("generate trace for rule:",fr)
    print("result:",TG.generateTrace(fr))

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