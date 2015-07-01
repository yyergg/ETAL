import os
import sys
import codecs
import config

def line_coverage():

##    # dump
##    os.system("adb logcat -d System.out:I *:S > "+os.path.join("templog.txt"))
##    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(config.getRoot())

    # get denominator
    denominator_lines = open("Denominator.txt").read().splitlines()

    # get numerator
    numeratorfile = open("templog.txt",'r')
    numerator_lines = numeratorfile.readlines()
    numeratorfile.close

    numeratorget = []
    for line in numerator_lines:
        if line.find("Linenumber: #")>0:
            numeratorget.append(line.split("Linenumber: #")[1].split(" Statement: #")[0])

    numeratorget.sort(key=int)
    numerator = []
    for line in numeratorget:
        if (numerator==[]):
            numerator.append(line)
        elif(line!=numerator[-1]):
            numerator.append(line)

    print("Line Coverage : ",100*len(numerator)/len(denominator_lines),"%")

def main():
    line_coverage()


if __name__ == "__main__":
    main()