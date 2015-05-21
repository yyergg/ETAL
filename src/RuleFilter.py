from Rule import RuleNode

def getSubtract(r1, r2):
    for c1 in r1.children:
        for c2 in r2.children:
            if c1.eventName == c2.eventName:
                getSubtract(c1,c2)

    removed = True
    for c1 in r1.children:
        if not c1.removed:
            removed = False

    if removed:
        r1.removed = True

        
        