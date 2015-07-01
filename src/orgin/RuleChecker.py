def ruleCheck(ruleInList, trace):

    #print("rulecheck",ruleInList,trace)
    i = 0
    j = 0
    while True:
        if j == len(trace):
            if i < len(ruleInList):
                return False
            else:
                return True
        elif trace[j] == ruleInList[i]:
            if i == len(ruleInList) - 1:
                return True
            i += 1
            j += 1
        else:
            j += 1
