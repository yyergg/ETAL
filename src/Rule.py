class RuleNode:
    eventName = ""
    children = []

    def __init__(self, eventname):
        self.eventName = eventname
        children = []