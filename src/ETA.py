import TraceGenerator
import TraceLoader
import RuleMiner
import RuleFilter
import RuleChecker
import WeightLearner
##import TaaDTCG
import TestingTask
import AdbExecutor
import os
import sys

TL = TraceLoader.TraceLoader()
TL.loadTrace("test")
TL.clusterTraces()
TL.printClusteredTrace()
##sys.exit(0)
RM = RuleMiner.RuleMiner()
RM.setTrace(TL.clusteredTraces["Pass"])
##print(TL.clusteredTraces["Pass"])
RM.setSupportThreshold(0.4)
RM.setConfidenceThreshold(0.5)
RM.miningRule()
print("Pass Rules:")
##RM.printRule(RM.rules,0)



failRuleSetDict = {}
for key, value in TL.clusteredTraces.items():
    if key != "Pass":
##        print(TL.clusteredTraces[key])
        RM2 = RuleMiner.RuleMiner()
        RM2.setTrace(TL.clusteredTraces[key])
        RM2.setSupportThreshold(0.4)
        RM2.setConfidenceThreshold(0.5)
        RM2.miningRule()
##        print("Fail rules = ",RM2.rules)
##        RM2.printRule(RM2.rules,0)
        # First Level Filter XOR - Remove pass rule which existing in fail rule from fail rule set
        RuleFilter.getSubtract(RM2.rules, RM.rules)
        print("Fail rules after 1-level filter:")
##        RM2.printRule(RM2.rules,0)
        ruleList = []
        for r in RM2.getAllRules(RM2.rules):
            ruleList.append(r)
        failRuleSetDict[key] = ruleList
        print(len(ruleList))
        print(":")
        print(ruleList)

# Second Level Filter - Apply fail rule on pass traces
i = 0
ratio = 0.1
for key,value in failRuleSetDict.items():
    while i < len(value):
        if len(value[i]) == 0:
            print("del", i)
            del value[i]
            continue
        counter = 0
        for t in TL.clusteredTraces["Pass"]:
            if RuleChecker.ruleCheck(value[i],t):
                counter += 1
                ratio = counter / len(TL.clusteredTraces["Pass"])
        if ratio > 0.05:
            del value[i]
            i -= 1
        i += 1
print("Fail rules after 2-level filter:")
print(value)


topFailRules = {}
for key, value in failRuleSetDict.items():
    # Weight Learninig
    WL = WeightLearner.WeightLearner(value,TL.clusteredTraces)
    WL.buildMatrix()
    WL.learn(key)
    if len(value) > 0:
        topFailRules[key] = WL.getTopRule()

traceInList = []
for key, value in TL.clusteredTraces.items():
    traceInList =  traceInList + value

##automatafolder = os.path.
##TGG = TaaDTCG.testcase(topFailRules[value],automatafolder)
##
##for key, value in failRuleSetDict.items():
##    for i in value:
##        for node in i
##            TGG.findShortestPath(,)

##TGG = TaaDTCG.TestCaseGenerator2(traceInList)



TG = TraceGenerator.TraceGenerator(traceInList)
TG.buildGraph()

text_file = open("../test/FailRule.txt","wb")

for key,value in topFailRules.items():
    print("generate trace for top rule of cluster:",key,value)
    print("Fail shortest path = ",TG.generateTrace(value))
    for idx, item in enumerate(TG.generateTrace(value)):
        if idx == len(TG.generateTrace(value))-1:
            text_file.write(bytes(str(item) + "",'UTF-8'))
        else:
            text_file.write(bytes(str(item) + " ",'UTF-8'))
##    text_file.write(value)
    text_file.close()
    text_file = open("../test/Output.txt","wb")
    for idx, item in enumerate(TG.generateTrace(value)):
        if idx == len(TG.generateTrace(value))-1:
            text_file.write(bytes(str(item) + "",'UTF-8'))
        else:
            text_file.write(bytes(str(item) + " ",'UTF-8'))
    text_file.close()


##print("result:",TG.generateTrace(value))


'''
example to test filter
R1 = RuleNode("A")
R2 = RuleNode("B")
R3 = RuleNode("C")
R4 = RuleNode("D")
R5 = RuleNode("E")

R6 = R1.children.append(R2)
## AB
R7 = R2.children.append(R4)
## BD
R8 = R1.children.append(R5)
## AE
R9 = R3.children.append(R4)
## CD
R10 = R1.children.append(R3)
## AC


R11 = R6..children.append(R5)
## ABE
R12 = R7.children.append(R5)
## BDE
R13 = R9.children.append(R5)
## CDE
R14 = R10.children.append(R4)

RM.printRule(R1,0)
RM.printRule(R4,0)

RuleFilter.getSubtract(R1,R4)

RM.printRule(R1,0)
'''