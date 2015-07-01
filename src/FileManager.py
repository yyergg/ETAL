#-------------------------------------------------------------------------------
# Name:        ?????1
# Purpose:
#
# Author:      b9890_000
#
# Created:     08/01/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import shutil
import json
import zipfile
import Config

class FileManager():
    def __init__(self,taskSetting,absSetting):
        self.root = Config.getRoot()
        self.userNameDir = os.path.join(self.root,"traces",taskSetting["userName"])
        self.appPackageNameDir = os.path.join(self.userNameDir,taskSetting["appPackageName"])
        self.versionFile = os.path.join(self.appPackageNameDir,"version.json")
        self.algorithm = taskSetting["algorithm"]
        self.version = taskSetting["version"]
        self.appPackageName = taskSetting["appPackageName"]
        self.absSetting = absSetting

        self.versionNum = 0
        self.abstractionNum = 0
        self.sessionNum = 0


    '''
    The followings are functions getting the all possible directories
    '''
    def getApkDir(self):
        return self.apkDir

    def getVersionDir(self):
        return self.versionDir

    def getAbstractionDir(self):
        return self.abstractionDir

    def getLabeledTraceDir(self):
        return self.labeledTraceDir

    def getSessionDir(self):
        return self.sessionDir

    def getVersionAutomataDir(self):
        return self.versionAutomataDir

    def getTraceSetDir(self):
        return self.traceSetDir

    def getSessionAutomataDir(self):
        return self.sessionAutomataDir

    '''
    The followings are getting the number of version, abstraction and session
    '''
    def getVersionNum(self):
        return self.versionNum

    def getAbstractionNum(self):
        return self.abstractionNum

    def getSessionNum(self):
        return self.sessionNum

    '''
    The followings are functions related to file manage
    '''
    def mkdir(self,path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def rmdir(self,path):
        if os.path.isdir(path):
            os.rmdir(path)

    def writeVersionFile(self):
        None

    def readIncrement(self,path):
        None

    def move(self,path1,path2):
        None

    '''
    The initialization
    '''
    def initialize(self):
        # handle userName
        if not os.path.isdir(self.userNameDir):
            self.mkdir(self.userNameDir)

        # handle appPackageName
        if not os.path.isdir(self.appPackageNameDir):
            self.mkdir(self.appPackageNameDir)

        # handle version
        if not os.path.isfile(self.versionFile): # first time
            with open(self.versionFile, "w") as outfile:
                self.versionNum = 1
                json.dump({'versionNum':1}, outfile, indent=4)

            self.versionDir = os.path.join(self.appPackageNameDir,"version1")
            self.mkdir(self.versionDir)
        else:
            versionFile_json = open(self.versionFile)
            versionFile = json.load(versionFile_json)
            versionFile_json.close()
            versionNum = versionFile["versionNum"]
            if self.version == "old":
                versionNum = int(versionNum)
                self.versionNum = versionNum
                self.versionDir = os.path.join(self.appPackageNameDir,"version"+str(versionNum))

            elif self.version == "new":
                versionNum = int(versionNum)+1
                self.versionNum = versionNum

                with open(self.versionFile, "w") as outfile:
                    json.dump({'versionNum':versionNum}, outfile, indent=4)

                self.versionDir = os.path.join(self.appPackageNameDir,"version"+str(versionNum))
                self.mkdir(self.versionDir)

            else:
                print("[Error] Invalid version. It should be new or old.")

        # handle abstraction
        self.abstractionFile = os.path.join(self.versionDir,"abstraction.json")
        if not os.path.isfile(self.abstractionFile): # first time
            with open(self.abstractionFile, "w") as outfile:
                self.abstractionNum = 1
                json.dump({'abstractionNum':1,'abstraction1':self.absSetting}, outfile, indent=4)

            self.abstractionDir = os.path.join(self.versionDir,"abstraction1")
            self.mkdir(self.abstractionDir)
        else:
            sameAbs = False
            abstractionFile_json = open(self.abstractionFile)
            abstractionFile = json.load(abstractionFile_json)
            abstractionFile_json.close()
            abstractionNum = abstractionFile["abstractionNum"]
            abstractionNum = int(abstractionNum)

            for i in range(1,abstractionNum+1):
                if self.absSetting == abstractionFile["abstraction"+str(i)]:
                    sameAbs = True
                    self.abstractionNum = i
                    self.abstractionDir = os.path.join(self.versionDir,"abstraction"+str(i))
                    break

            if not sameAbs:
                abstractionNum += 1
                self.abstractionNum = abstractionNum

                with open(self.abstractionFile, "w") as outfile:
                    data = {'abstractionNum':abstractionNum}
                    for i in range(1,abstractionNum):
                        data['abstraction'+str(i)] = abstractionFile['abstraction'+str(i)]
                    data['abstraction'+str(abstractionNum)] = self.absSetting
                    json.dump(data, outfile, indent=4)

                self.abstractionDir = os.path.join(self.versionDir,"abstraction"+str(abstractionNum))
                self.mkdir(self.abstractionDir)

        # labeledTrace/ and sessionX/ is mutually exclusive.
        if self.algorithm == "SELabeler":
            # handle the labeledTrace for SELabeler
            self.labeledTraceDir = os.path.join(self.abstractionDir,"labeledTrace")
            if not os.path.isdir(self.labeledTraceDir): # should be always true
                self.mkdir(self.labeledTraceDir)

            # handle traceSet
            self.traceSetDir = os.path.join(self.labeledTraceDir,"traceSet")
            if not os.path.isdir(self.traceSetDir): # should be always true
                self.mkdir(self.traceSetDir)

            # handle sessionAutomata
            self.sessionAutomataDir = os.path.join(self.labeledTraceDir,"sessionAutomata")
            if not os.path.isdir(self.sessionAutomataDir): # should be always true
                self.mkdir(self.sessionAutomataDir)

        else:
            # handle session
            self.sessionFile = os.path.join(self.abstractionDir,"session.json")
            if not os.path.isfile(self.sessionFile): # first time
                with open(self.sessionFile, "w") as outfile:
                    self.sessionNum = 1
                    json.dump({'sessionNum':1,'coveredSession':[]}, outfile, indent=4)

                self.sessionDir = os.path.join(self.abstractionDir,"session1")
                self.mkdir(self.sessionDir)
            else:
                sessionFile_json = open(self.sessionFile)
                sessionFile = json.load(sessionFile_json)
                sessionFile_json.close()
                sessionNum = sessionFile["sessionNum"]
                sessionNum = int(sessionNum)+1
                self.sessionNum = sessionNum
                coveredSession = sessionFile["coveredSession"]

                with open(self.sessionFile, "w") as outfile:
                    json.dump({'sessionNum':sessionNum,'coveredSession':coveredSession}, outfile, indent=4)

                self.sessionDir = os.path.join(self.abstractionDir,"session"+str(sessionNum))
                self.mkdir(self.sessionDir)

            # handle versionAutomata
            self.versionAutomataDir = os.path.join(self.abstractionDir,"versionAutomata")
            if not os.path.isdir(self.versionAutomataDir): # should be always true
                self.mkdir(self.versionAutomataDir)

            # handle traceSet
            self.traceSetDir = os.path.join(self.sessionDir,"traceSet")
            if not os.path.isdir(self.traceSetDir): # should be always true
                self.mkdir(self.traceSetDir)

            # handle sessionAutomata
            self.sessionAutomataDir = os.path.join(self.sessionDir,"sessionAutomata")
            if not os.path.isdir(self.sessionAutomataDir): # should be always true
                self.mkdir(self.sessionAutomataDir)







