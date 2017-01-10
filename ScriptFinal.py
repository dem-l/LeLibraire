import os
import sys
import csv 
import time 
import datetime 

wekaJarPath = "lib/weka.jar" 

# ----- Processing Data Methods ----- #	
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
	os.system("java -cp " + wekaJarPath + " weka.core.converters.CSVLoader "+ifn+" -B 10000 > "+ofn)
	return;
	
def replaceSeps (ifn, ofn):
	f = open(ifn, 'rb')
	f1 = open(ofn, 'wb')
	reader = csv.reader(f, delimiter=';')
	writer = csv.writer(f1, delimiter=',')
	for row in reader:
		writer.writerow(row)
	
def convertDate (ifn, ofn, numberClass):
	f = open(ifn, 'rb') 
	f1 = open(ofn, 'wb')
	reader = csv.reader(f, delimiter=',')
	writer = csv.writer(f1, delimiter=',')
	writer.writerow(reader.next())

	for row in reader: 
		row[numberClass] = time.mktime(datetime.datetime.strptime(row[numberClass], "%d/%m/%Y").timetuple())
		writer.writerow(row)

def standardize (ifn, ofn):
	os.system("java -cp " + wekaJarPath + " weka.filters.unsupervised.attribute.Standardize -i "+ifn+" -o "+ofn)

def nominalToBinary(ifn, ofn):
	os.system("java -cp " + wekaJarPath + " weka.filters.supervised.attribute.NominalToBinary -c 23 -i " + ifn + " -o " + ofn)


# ----- Cut Data ----- #
def cutData(corpusFilename, trainFilename, devFilename, testFilename):
	tmp_filename = "40percent_data.arff";

	os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 60 -B 0 -S 1 -i " + corpusFilename + " -c 44 -no-replacement -o " + trainFilename)
	print("inf | Fichier d'entrainement cree")

	os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 60 -B 0 -S 1 -i " + corpusFilename + " -c 44 -V -no-replacement -o " + tmp_filename)	
 
	os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 50 -B 0 -S 1 -i " + tmp_filename + " -c 44 -no-replacement -o " + devFilename)
	print("inf | Fichier de validation cree")

	os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 50 -B 0 -S 1 -i " + tmp_filename + " -c 44 -V -no-replacement -o " + testFilename)
	print("inf | Fichier de test cree")


# ----- Train Methods ----- #
def preparation1(corpus, trainFilename, devFilename, testFilename):
	dataFilename = corpus 
	pointerFilename = dataFilename
	basename_inputFilename = dataFilename.split('.')[0]
	extension_inputFilename = dataFilename.split('.')[1] 

	print("Etape 1 | Preparation des donnees ")
	print("Etape 1.1 | Transformation du fichier csv ',' en ';'")
	sepsFilename = basename_inputFilename + "_SEPS." + extension_inputFilename
	replaceSeps(dataFilename, sepsFilename)
	pointerFilename = sepsFilename;
	print("inf | fichier " + pointerFilename + " cree")
	
	print("Etape 1.2 | Suppression des instances avec une valeur NA dans un de leur champs.")
	rzFilename = basename_inputFilename + "_RZ." + extension_inputFilename
	removeZeros(pointerFilename, rzFilename)
	pointerFilename = rzFilename
	print("inf | fichier " + pointerFilename + " cree")

	print("Etape 1.3 | Transformation de la date en timestamp")
	timestampFilename = basename_inputFilename + "_timestamp." + extension_inputFilename
	convertDate(pointerFilename, timestampFilename, 8)
	pointerFilename = timestampFilename
	print("inf | fichier " + pointerFilename + " cree")
		

	print("Etape 1.4 | Transformation du fichier en arff")
	arffFilename = basename_inputFilename+".arff"
	convertToArff (pointerFilename, arffFilename)
	pointerFilename = arffFilename
	print("info | fichier " + pointerFilename + " cree")
		
	print("Etape 1.5 | NominalToBinary -c 23")
	ntbFilename = basename_inputFilename + "_NTB.arff"
	nominalToBinary(pointerFilename, ntbFilename)
	pointerFilename = ntbFilename
	print("inf | fichier " + pointerFilename + " cree")
	
	print
	print("Etape 2 | Decoupage du corpus")
	cutData(pointerFilename, trainFilename, devFilename, testFilename)


# ----- Models ----- #
def model1(trainFilename, devFilename, testFilename, modelDir): 
	print
	print("Etape 3 | Creation du model ")
	modelFilename = "modelTrained.model"
	trainOutputFilename = "trainOutput.txt"
	os.system("java -cp " + wekaJarPath + " weka.classifiers.bayes.BayesNet -c 44 -t " + trainFilename + " -d " + modelDir + modelFilename + " > " + modelDir + trainOutputFilename)
	print("inf | Model cree, fichier accessible " + modelDir)	
	
	print
	print("Etape 4 | Validation") 
	print("inf | En cours de developpement")

	print
	print("Etape 5 | Test du model ") 
	print("inf | En cours de developpement")
 	os.system("java -cp " + wekaJarPath + " weka.classifiers.bayes.BayesNet -l " + modelDir + modelFilename + " -T " + testFilename)


# ----- MAIN ----- #
def main ():
	corpus = "data/KTFGHU14.csv"
	prep1_trainFilename = "data/KTFGHU14_train.arff"
	prep1_devFilename = "data/KTFGHU14_dev.arff"
	prep1_testFilename = "data/KTFGHU14_test.arff"

	preparation1(corpus, prep1_trainFilename, prep1_devFilename, prep1_testFilename)
	model1(prep1_trainFilename, prep1_devFilename, prep1_testFilename, "models/model1/")

main()
