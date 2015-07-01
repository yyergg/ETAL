#-------------------------------------------------------------------------------
# Name:        ??蝛??1
# Purpose:
#
# Author:      b9890_000
#
# Created:     10/04/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys

class CoverageInformation:
    def __init__(self,versionDir,isInstrument):
        self.isInstrument = isInstrument
        if self.isInstrument:
            self.Denominator = self.getDenominator(versionDir)

        self.numeratorList = []
        self.Numerator = 0
        self.lineCoverage = 0

    def getLineCoverage(self):
        return self.lineCoverage

    def caculate(self,coveragePath):
        if self.isInstrument:
            # get numerator
            numeratorfile = open(coveragePath,'r')
            numerator_lines = numeratorfile.readlines()
            numeratorfile.close

            for line in numerator_lines:
                if line.find("Linenumber: #")>0:
                    lineNum = int(line.split("Linenumber: #")[1].split(" Statement: #")[0])
                    if lineNum not in self.numeratorList:
                        self.numeratorList.append(lineNum)

            self.Numerator = len(self.numeratorList)
            if self.Denominator != 0:
                self.lineCoverage = 100*(self.Numerator)/self.Denominator
                print("Line coverage = ",self.lineCoverage," %")
            else:
                print("Can't calculate line coverage because the Denominator is zero.")
        else:
            pass

    def getDenominator(self,versionDir):
        if os.path.isfile(os.path.join(versionDir,"Denominator.txt")):
            denominator_lines = open(os.path.join(versionDir,"Denominator.txt")).read().splitlines()
        else:
            print("Can't find the Denominator.txt file.")
            print("Maybe you use a new version without the instrumentation.")
            print("Or maybe instrumentation failure.")
            sys.exit(0)

        return len(denominator_lines)



