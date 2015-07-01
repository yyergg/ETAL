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

from AutomataManager import AutomataManager
from abstraction import Abstraction
import os
import json

class VersionAutomata():
    def __init__(self,taskSetting):
        self.root = ""
        self.userName = taskSetting["userName"]
        self.appPackageName = taskSetting["appPackageName"]
        self.versionNum = taskSetting["versionNum"]
        self.abstractionNum = taskSetting["abstractionNum"]
        self.isReset = taskSetting["reset"]
        self.targetSessionList = taskSetting["targetSession"]
        # parent path is username + package name
        self.parentPath = os.path.join(self.root,self.userName,self.appPackageName)

        # get abstraction
        self.versionDir = os.path.join(self.root,self.userName,self.appPackageName,"version"+str(self.versionNum))
        self.abstractionFilePath = os.path.join(self.versionDir,"abstraction.json")
        abstraction_json = open(self.abstractionFilePath)
        self.abstractionFile = json.load(abstraction_json)
        abstraction_json.close()
        self.abs = self.abstractionFile["abstraction"+str(self.abstractionNum)]
        print(self.abs)

        # new a abstraction object
        self.abstraction = Abstraction()
        self.abstraction.setAbstraction(self.abs)

        # get our Automata Manager
        self.am = AutomataManager(self.abstraction)
        # It is important to set the parent path in order to access the correct xml files.
        self.am.setParentPath(self.parentPath)


    def generateAutomata(self):
        abstractionDir = os.path.join(self.root,self.userName,self.appPackageName,\
                                           "version"+str(self.versionNum),\
                                           "abstraction"+str(self.abstractionNum))
        if self.isReset == "True":
            self.am.newTrace()
            # 1.for session in target: load sessionAutomata
            for session in self.targetSessionList:
                sessionDir = os.path.join(abstractionDir,"session"+str(session),"traceSet")
                self.am.loadSession(sessionDir)


            # 2.update session.json
            sessionFile = os.path.join(abstractionDir,"session.json")
            session_json = open(sessionFile)
            sessionData = json.load(session_json)
            session_json.close()
            sessionData["coveredSession"] = self.targetSessionList

            with open(sessionFile,'w') as outFile:
                json.dump(sessionData,outFile,indent=4)

            # 3.save the version automata
            automataDir = os.path.join(abstractionDir,"versionAutomata")
            self.am.saveAutomata(automataDir)


        else:
            self.am.newTrace()
            # 1.get covered sessions
            sessionFile = os.path.join(abstractionDir,"session.json")
            session_json = open(sessionFile)
            sessionData = json.load(session_json)
            session_json.close()
            coveredSession = sessionData["coveredSession"]

            # 2.for session in coveredSession: load sessionAutomata
##            for session in coveredSession:
##                automataDir = os.path.join(abstractionDir,"session"+str(session),"sessionAutomata")
##                self.am.loadAutomata(automataDir)
            for session in coveredSession:
                sessionDir = os.path.join(abstractionDir,"session"+str(session),"traceSet")
                self.am.loadSession(sessionDir)


            # 3.update automata by each target not in covered
            for session in self.targetSessionList:
                if session not in coveredSession:
                    sessionDir = os.path.join(abstractionDir,"session"+str(session),"traceSet")
                    self.am.loadSession(sessionDir)
                    coveredSession.append(session)

            # 4.update session.json
            sessionData["coveredSession"] = coveredSession

            with open(sessionFile,'w') as outFile:
                json.dump(sessionData,outFile,indent=4)

            # 5.save the version automata
            automataDir = os.path.join(abstractionDir,"versionAutomata")
            self.am.saveAutomata(automataDir)










