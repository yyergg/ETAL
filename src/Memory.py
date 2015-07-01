#-------------------------------------------------------------------------------
# Name:        ??穿??1
# Purpose:
#
# Author:      b9890_000
#
# Created:     14/04/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class MemoryInformation:
    def __init__(self):
        pass

    def parse(self,path):
        memInfo = open(path)
        lines = memInfo.readlines()
        memInfo.close()

        for line in lines:
            #     TOTAL     6540     4888      588        0    14368     7800     6567
            line = line.strip(" ").replace("\n","").split(" ")

            if len(line) > 1:
                # remove ""
                line = [x for x in line if x != ""]
                if line[0] == "TOTAL":
                    self.pssTotal = line[1]
##                    self.privateDirty = line[2]
##                    self.privateClean = line[3]
##                    self.swappedDirty = line[4]
##                    self.heapSize = line[5]
##                    self.heapAlloc = line[6]
##                    self.heapFree = line[7]
                    print("proportional set size(pss) = ",self.pssTotal," KB")

















