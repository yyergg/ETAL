def ruleCheck(ruleInList, trace):

    #print("rulecheck",ruleInList,trace)
    i = 0
    j = 0
    while True:
        #print(i,j,ruleInList[i],trace[j])
        if j == len(trace) - 1 and i < len(ruleInList):
            return False
        elif trace[j] == ruleInList[i]:
            if i == len(ruleInList)-1:
                return True
            i += 1
            j += 1
        else:
            if j == len(trace) - 1:
                return False
            j += 1


def ruleCheck2(ruleInList, trace):

    #print("rulecheck",ruleInList,trace)
    i = 0
    j = 0
    count = 0
    while True:
        #print(i,j,ruleInList[i],trace[j])
        if j == len(trace) - 1 and i < len(ruleInList):
            return False
        elif trace[j] == ruleInList[i]:
            count += 1
            if i == len(ruleInList)-1:
                if count >= 2:
                    return True
                else:
                    return False
            i += 1
            j += 1
        else:
            if j == len(trace) - 1:
                return False
            j += 1
