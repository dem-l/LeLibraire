import os
import sys
	
def removeZeros (ifn, ofn):
	f = open(ifn, 'rb')
	f1 = open(ofn, 'wb')
	reader = csv.reader(f, delimiter=',')
	writer = csv.writer(f1)
	writer.writerow (reader.next())
	for row in reader:
		if row[2] != 'NA' and row[5] != 'NA':
			writer.writerow (row)
	return;
	
def convertToArff (ifn, ofn):
	os.system("java -cp weka.jar weka.core.converters.CSVLoader "+ifn+" -B 10000 > "+ofn)
	return;
	
def replaceSeps (ifn, ofn):
	basename_ifn = ifn.split('.')[0]
	extension_ifn = ifn.split('.')[1]
	ofn = basename_ifn+"_replacedSeps."+extension_ifn
	
	with open(ifn, 'rb') as f:
		content = f.readlines()
	with open(ofn, 'wb') as f1:
		writer = csv.writer(f1)
		for row in content:
			writer.writerow (row.replace(';',','))
	
def standardize (ifn, ofn):
	os.system("java -cp ../lib/weka.jar weka.filters.unsupervised.attribute.Standardize -i "+ifn+" -o "+ofn)
	
def main ():
	inputFilename=""
	if len(sys.argv)==2 and sys.argv[1]:
		inputFilename = sys.argv[1]
		
		replacedSeps_filename = ''
		replaceSeps (inputFilename, replacedSeps_filename)
		
		basename_inputFilename = inputFilename.split('.')[0]
		extension_inputFilename = inputFilename.split('.')[1]
		
		inputFilenameWoZeros = basename_inputFilename+"-wozeros."+extension_inputFilename
		removeZeros (replacedSeps_filename, inputFilenameWoZeros)
		
		arffFilename = basename_inputFilename+".arff"
		convertToArff (inputFilenameWoZeros, arffFilename)
	
