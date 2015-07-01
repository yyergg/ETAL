class RuleNode:
    eventName = ""
    children = []
    removed = False

    def __init__(self, eventname):
        self.eventName = eventname
        self.children = []

class Weight:
    def __init__(self):
        self.weight = []
        self.threshold = 0
        self.score = 0
        self.fresh = True

class GraphNode:
    def __init__(self,name):
        self.name = name
        self.children = []
        self.BFSParent = None