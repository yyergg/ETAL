import TraceLoader
import RuleMiner
import os


TL = TraceLoader.TraceLoader()
TL.loadTrace("test\\trace0")
TL.clusterTraces()


RM = RuleMiner.RuleMiner()
RM.setTrace(TL.clusteredTraces["Pass"])
#RM.setTraceTest()
RM.miningRule()
RM.printRule(RM.rules,0)

