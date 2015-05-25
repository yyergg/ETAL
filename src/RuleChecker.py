def ruleCheck(ruleInList, trace):
    i = 0
    j = 0
    while True:
        if trace[j] == ruleInList[i]:
            if i == len(ruleInList)-1:
                return True
            i += 1
            j += 1
        else:
            if j == len(trace) - 1:
                return False
            j += 1
