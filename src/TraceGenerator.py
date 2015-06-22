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
        ruleInList = ["0"] + ruleInList
        newTrace = []
        i = 0
        while i < len(ruleInList) - 1:
            newTrace = newTrace + self.findShortestPath(ruleInList[i],ruleInList[i+1])
            #print(self.findShortestPath(ruleInList[i],ruleInList[i+1]))
            i += 1
        newTrace.append(ruleInList[-1])
        return newTrace

    def traverseBack(self,dst):
        result = []
        while dst.BFSParent != None:
            print(dst.BFSParent.name)
            result.append(dst.name)
            dst = dst.BFSParent
        result.append(dst.name)
        result.reverse()
        result = result[:-1]
        return result

    def findShortestPath(self, src, dst):
        print("find shortest path",src,dst)
        for key,value in self.nodeMap.items():
            value.BFSParent = None
        visited = []
        visited.append(src)
        frontier = []
        frontier.append(self.nodeMap[src])
        counter = 0
        while counter < len(self.nodeMap):
            nextFrontier = []
            for i in frontier:
                for child in i.children:
                    #print(i.name,"->",child.name)
                    if child.name not in visited:
                        visited.append(child.name)
                        child.BFSParent = i
                        if child.name == dst:
                            return self.traverseBack(child)
                        else:
                            nextFrontier.append(child)
            frontier = nextFrontier
            counter += 1