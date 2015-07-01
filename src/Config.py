#-------------------------------------------------------------------------------
# Name:        ??1
# Purpose:
#
# Author:      b9890_000
#
# Created:     08/01/2015
# Copyright:   (c) b9890_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os

def getRoot():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def getBin():
    return os.path.join(getRoot(),"bin")

def getSUT():
    return os.path.join(getRoot(),"SUT")