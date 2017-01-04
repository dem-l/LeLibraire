import os
import sys
import csv
import arff

data=arff.load('data/donnees.arff')
os.system('java -version')
print 'File name : ', sys.argv[1]