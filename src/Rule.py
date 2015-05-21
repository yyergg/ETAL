class RuleNode:
    eventName = ""
    children = []
    removed = False

    def __init__(self, eventname):
        self.eventName = eventname
        self.children = []