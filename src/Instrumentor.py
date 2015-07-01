#-------------------------------------------------------------------------------
# Name:        ?????1
# Purpose:
#
# Author:      b9890_000
#
# Created:     08/04/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys
import zipfile
import shutil
import subprocess
import Config
from Coverage import CoverageInformation

class Instrumentor():
    def __init__(self,taskSetting,versionDir):
        self.doInstrument = taskSetting["instrument"]
        self.apkFile = taskSetting["apkFile"]
        self.appPackageName = taskSetting["appPackageName"]
        self.versionDir = versionDir

    def isInstrument(self):
        if self.doInstrument == "yes" or self.doInstrument == "already":
            return True
        else:
            return False

    def instrument(self):
        if self.doInstrument == "yes":
            print("Start Instrument.")

            # 1. instrument SUT
            self.binDir = Config.getBin()
            self.SUTDir = Config.getSUT()
            cmd = "java -Xmx1000m -cp "+self.binDir+";"+os.path.join(self.binDir,"soot-trunk.jar")+" AndroidInstrument -allow-phantom-refs -android-jars "+os.path.join(self.binDir,"android-platforms-master")+" -process-dir "+ os.path.join(self.SUTDir,self.apkFile)+" -output-dir "+os.path.join(self.binDir,"sootOutput")
            print("1. instrument SUT....")
            print("    cmd = "+cmd)
            os.system(cmd)

            # 2. sign in the instrumented apk
            self.instrumentedAPK = os.path.join(self.binDir,"sootOutput",self.apkFile)
            cmd = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "+os.path.join(self.binDir,"my-release-key.keystore")+" "+self.instrumentedAPK+" alias_name"
            print("2. sign in the instrumented apk....")
            print("    cmd = "+cmd)
            s = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell =True)
            s.communicate(input = bytes("abc123", 'UTF-8'))

            # 3. uninstall the original apk
            cmd = "adb uninstall "+self.appPackageName
            print("3. uninstall the original apk....")
            print("    cmd = "+cmd)
            os.system(cmd)

            # 4. install instrumented apk into the device
            #self.instrumentedAPK = os.path.join(Config.getSUT(),self.apkFile)
            cmd = "adb install "+self.instrumentedAPK
            print("4. install instrumented apk into the device....")
            print("    cmd = "+cmd)
            os.system(cmd)

            # 5.  place the instrumented APK file and Denominator.txt in the version directory
            print("5. place the instrumented APK file and Denominator.txt in the version directory....")
            if os.path.isfile(self.instrumentedAPK):
                shutil.copy(self.instrumentedAPK,self.versionDir)
            else:
                print("Can not find the instrumented APK file.")
                sys.exit(0)

            if os.path.isfile("Denominator.txt"):
                if os.path.isfile(os.path.join(self.versionDir,"Denominator.txt")):
                    os.remove(os.path.join(self.versionDir,"Denominator.txt"))
                shutil.move("Denominator.txt",self.versionDir)
            else:
                print("Can not find the Denominator.txt.")
                sys.exit(0)

            print("Instrument completely.")
        elif self.doInstrument == "already":
            print("Already instrument.")
        else:
            print("Do not instrument.")








