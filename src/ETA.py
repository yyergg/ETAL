import TraceLoader
import RuleMiner
import RuleFilter
import RuleChecker
import WeightLearner
import os


TL = TraceLoader.TraceLoader()
TL.loadTrace("test/trace0")
TL.clusterTraces()
TL.printClusteredTrace()

print("Pass Rules:")
RM = RuleMiner.RuleMiner()
RM.setTrace(TL.clusteredTraces["Pass"])
RM.setSupportThreshold(0.2)
RM.setSupportThreshold(0.2)
RM.miningRule()
RM.printRule(RM.rules,0)

print("Fail Rules:")
RM2 = RuleMiner.RuleMiner()
RM2.setTrace(TL.clusteredTraces["Fail"])
RM2.setSupportThreshold(0.6)
RM2.setSupportThreshold(0.5)
RM2.miningRule()
RM2.printRule(RM2.rules,0)

print("Fail Rules after filter:")
RuleFilter.getSubtract(RM2.rules, RM.rules)
RM2.printRule(RM2.rules,0)

failRuleset = []
for r in RM2.getAllRules(RM2.rules):
    failRuleset.append(r)

WL = WeightLearner.WeightLearner(failRuleset,TL.clusteredTraces)
WL.printPopulation()
WL.calculateScore("Fail")
WL.printPopulation()


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