import sys 
import csv 
import os

filepath = sys.argv[1] 
filepathWithoutExt = os.path.splitext(filepath)[0] 

filepath_train = filepathWithoutExt + "_train.csv"
filepath_dev = filepathWithoutExt = "_dev.csv"
filepath_test = filepathWithoutExt = "_test.csv"


f = open(filename, 'rb')
reader = csv.reader(f, delimiter=';')

for row in reader:
	if row[2] != 'NA' and row[5] != 'NA':
		writer.writerow (row)