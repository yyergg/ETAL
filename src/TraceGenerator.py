from DataStructure import GraphNode

class TraceGenerator:
    def __init__(self,traces = []):
        self.traces = traces
        self.graph = None
        self.nodeMap = {}

    def setTraces(self,traces):
        self.traces = traces

    def buildGraph(self):
        self.nodeMap = {}
        for trace in self.traces:
            i = 0
            while i < len(trace):
                if trace[i] not in self.nodeMap:
                    self.nodeMap[trace[i]] = GraphNode(trace[i])
                if i != 0:
                    self.nodeMap[trace[i-1]].children.append(self.nodeMap[trace[i]])
                i += 1

    def generateTrace(self,ruleInList):
        newTrace = []
        i = 2
        while i < len(ruleInList):
            newTrace.append(ruleInList[i-2])
            newTrace.append(ruleInList[i-1])
            newTrace = newTrace + self.findShortestPath(ruleInList[i-1],ruleInList[i])
            i += 2
        return newTrace

    def traverseBack(self,dst):
        result = []
        while dst.BFSParent != None:
            result.append(dst.name)
            dst = dst.BFSParent
        return result

    def findShortestPath(self, src, dst):
        print("find shortest path",src,dst)

        for key,value in self.nodeMap.items():
            value.BFSParent = None

        visited = []
        frontier = []
        frontier.append(self.nodeMap[src])
        while True:
            nextFrontier = []
            for i in frontier:
                for child in i.children:
                    #print(i.name,"->",child.name)
                    if child.name not in visited:
                        visited.append(child.name)
                        child.BFSParent = i
                        if child.name == dst:
                            return self.traverseBack(i)
                        else:
                            nextFrontier.append(child)
            frontier = nextFrontier