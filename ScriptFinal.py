import os
import sys
import csv
import time
import datetime
import types

wekaJarPath = "lib/weka.jar"

# ----- Processing Data Methods ----- #
def removeZeros(ifn, ofn):
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
	print(ifn)
	print(ofn)
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
	if(not os.path.exists(trainFilename)):
		os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 60 -B 0 -S 1 -i " + corpusFilename + " -c 44 -no-replacement -o " + trainFilename)
		print("inf | Fichier d'entrainement cree")

	if(not os.path.exists(devFilename) or not os.path.exists(testFilename)):
		os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 60 -B 0 -S 1 -i " + corpusFilename + " -c 44 -V -no-replacement -o " + tmp_filename)	
 
	if(not os.path.exists(devFilename)):
		os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 50 -B 0 -S 1 -i " + tmp_filename + " -c 44 -no-replacement -o " + devFilename)
		print("inf | Fichier de validation cree")

	if(not os.path.exists(testFilename)):
		os.system("java -cp " + wekaJarPath + " weka.filters.supervised.instance.Resample -Z 50 -B 0 -S 1 -i " + tmp_filename + " -c 44 -V -no-replacement -o " + testFilename)
		print("inf | Fichier de test cree")


# ----- Train Methods ----- #
def preparation1(corpus, trainFilename, devFilename, testFilename):
	if(not os.path.exists(trainFilename) or not os.path.exists(devFilename) or not os.path.exists(testFilename)):
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

# ----- Fonction utilisant le modele Bayes Naif ----- #
def model1(trainFilename, devFilename, testFilename, modelDir, classNumber): 
	print
	print("Etape 3 | Creation du model BayesNet")
	modelFilename = "modelTrained.model"
	trainOutputFilename = "trainOutput.txt"
	os.system("java -cp " + wekaJarPath + " weka.classifiers.bayes.BayesNet -c " + classNumber + " -t " + trainFilename + " -d " + modelDir + modelFilename + " > " + modelDir + trainOutputFilename)
	print("inf | Model cree, fichier accessible " + modelDir)	
	
	print
	print("Etape 4 | Validation") 
	print("inf | En cours de developpement")

	
	print
	print("Etape 5 | Test du model ") 
	print("inf | En cours de developpement")
	os.system("java -cp " + wekaJarPath + " weka.classifiers.bayes.BayesNet -l " + modelDir + modelFilename + " -T " + testFilename)

# ----- Fonction utilisant le modele MultilayerPerceptron ----- #
def model2(trainFilename, devFilename, testFilename, modelDir, classNumber):
	print
	print("Etape 3 | creation du model ")
	modelFilename = "modelTrained.model"
	trainOutputFilename = "trainOutput.txt"
	thresholdOutputFilename = "thresholdOutput.arff"
	thresholdOutputFilenameCSV = "thresholdOutput.csv"
	classificationOutputFilename = "classificationOutput.csv"
	testPrefix = "test-"
	# Options
	# -L x : Taux d'apprentissage 
	# -M x : Taux de momentum 
	# -N x : Nombre d'iterations a effectuer
	# -V x : Taille du pourcentage de validation fixee pour utiliser 
	# -S x : valeur utilisee pour seeder le generateur aleatoire
	# -E x : Threshold pour le nombre d'erreurs consecutives
	# -H letter : 
	# -c : index de la classe
	
	defaultL = 0.3
	defaultM = 0.3
	defaultN = 20
	i=0
	while i<=9:
		value = 0.1+0.1*i
		print ("creation du model avec L = "+str(value))
		prefix = "L_" + str(value) + "-"
		if not os.path.exists(modelDir + prefix + modelFilename) or not os.path.exists(modelDir + prefix + trainOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -L " + str(value) + " -M " + str(defaultM) + " -N " + str(defaultN) + " -V 0 -S 0 -E 20 -H a -c " + classNumber + " -t " + trainFilename + " -d " + modelDir + prefix + modelFilename + " > " + modelDir + prefix + trainOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilename) or not os.path.exists(modelDir + prefix + classificationOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -l " + modelDir + prefix + modelFilename + " -T " + devFilename + " -threshold-file " + modelDir + prefix + thresholdOutputFilename + " -threshold-label Yes -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" > " + modelDir + prefix + classificationOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilenameCSV):
			os.system("java -cp " + wekaJarPath + " weka.core.converters.CSVSaver -i " + modelDir + prefix + thresholdOutputFilename + " -o " + modelDir + prefix + thresholdOutputFilenameCSV + " -F ,")
		i += 1
	i=0
	while i<=9:
		value = 0.1+0.1*i
		print ("creation du model avec M = "+str(value))
		prefix = "M_" + str(value) + "-"
		if not os.path.exists(modelDir + prefix + modelFilename) or not os.path.exists(modelDir + prefix + trainOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -L " + str(defaultL) + " -M "+str(value)+" -N " + str(defaultN) + " -V 0 -S 0 -E 20 -H a -c " + classNumber + " -t " + trainFilename + " -d " + modelDir + prefix + modelFilename + " > " + modelDir + prefix + trainOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilename) or not os.path.exists(modelDir + prefix + classificationOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -l " + modelDir + prefix + modelFilename + " -T " + devFilename + " -threshold-file " + modelDir + prefix + thresholdOutputFilename + " -threshold-label Yes -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" > " + modelDir + prefix + classificationOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilenameCSV):
			os.system("java -cp " + wekaJarPath+ " weka.core.converters.CSVSaver -i " + modelDir + prefix + thresholdOutputFilename + " -o " + modelDir + prefix + thresholdOutputFilenameCSV + " -F ,")
		i += 1
	i=10
	while i<=500:
		value = i
		print ("creation du model avec N = "+str(value))
		prefix = "N_" + str(value) + "-"
		if not os.path.exists(modelDir + prefix + modelFilename) or not os.path.exists(modelDir + prefix + trainOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -L " + str(defaultL) + " -M " + str(defaultM) + " -N "+str(value)+" -V 0 -S 0 -E 20 -H a -c " + classNumber + " -t " + trainFilename + " -d " + modelDir + prefix + modelFilename + " > " + modelDir + prefix + trainOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilename) or not os.path.exists(modelDir + prefix + classificationOutputFilename):
			os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -l " + modelDir + prefix + modelFilename + " -T " + devFilename + " -threshold-file " + modelDir + prefix + thresholdOutputFilename + " -threshold-label Yes -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" > " + modelDir + prefix + classificationOutputFilename)
		if not os.path.exists(modelDir + prefix + thresholdOutputFilenameCSV):
			os.system("java -cp " + wekaJarPath+ " weka.core.converters.CSVSaver -i " + modelDir + prefix + thresholdOutputFilename + " -o " + modelDir + prefix + thresholdOutputFilenameCSV + " -F ,")
		i += 50
	print
	print("Etape 4 | Validation ")
	print("Calul des f-mesures")

	maxFMeasure = 0
	maxPrefix = ""
	maxThreshold = 0

	i=0
	while i<=9:
		value = 0.1+0.1*i
		prefix = "L_" + str(value) + "-"
		result = calculPerformance(modelDir + prefix + thresholdOutputFilenameCSV)
		if float(result[9]) > maxFMeasure:
			maxFMeasure = float(result[9])
			maxPrefix = prefix
			maxThreshold = float(result[12])
		print(prefix + " : " + str(result[0]) + " => " + result[9] + "(FMeasure) => " + result[12] + "(Threshold)")
		i += 1
	i=0

	while i<=9:
		value = 0.1+0.1*i
		prefix = "M_" + str(value) + "-"
		result = calculPerformance(modelDir + prefix + thresholdOutputFilenameCSV)
		if float(result[9]) > maxFMeasure:
			maxFMeasure = float(result[9])
			maxPrefix = prefix
			maxThreshold = float(result[12])
		print(prefix + " : " + str(result[0]) + " => " + result[9] + "(FMeasure) => " + result[12] + "(Threshold)")
		i += 1

	i=10
	while i<=500:
		value = i
		prefix = "N_" + str(value) + "-"
		result = calculPerformance(modelDir + prefix + thresholdOutputFilenameCSV)
		if float(result[9]) > maxFMeasure:
			maxFMeasure = float(result[9])
			maxPrefix = prefix
			maxThreshold = float(result[12])
		print(prefix + " : " + str(result[0]) + " => " + result[9] + "(FMeasure) => " + result[12] + "(Threshold)")
		i += 50

	print
	print("Meilleur modele en dev : " + str(maxPrefix) + " avec un FMeasure de " + str(maxFMeasure) + " et un seuil de " + str(maxThreshold))

	print 
	print("Etape 5 | Test du model " + maxPrefix)

	noThreshold = 1 - maxThreshold
	os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -l " + modelDir + maxPrefix + modelFilename + " -T " + testFilename + " -threshold-file " + modelDir + testPrefix + "yes-" + thresholdOutputFilename + " -threshold-label Yes -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" > " + modelDir + testPrefix + "yes-" + classificationOutputFilename)
	os.system("java -cp " + wekaJarPath+ " weka.core.converters.CSVSaver -i " + modelDir + testPrefix + "yes-" + thresholdOutputFilename + " -o " + modelDir + testPrefix + "yes-" + thresholdOutputFilenameCSV + " -F ,")

	os.system("java -cp " + wekaJarPath + " weka.classifiers.functions.MultilayerPerceptron -l " + modelDir + maxPrefix + modelFilename + " -T " + testFilename + " -threshold-file " + modelDir + testPrefix + "no-" + thresholdOutputFilename + " -threshold-label No -classifications \"weka.classifiers.evaluation.output.prediction.CSV\" > " + modelDir + testPrefix + "no-" + classificationOutputFilename)
	os.system("java -cp " + wekaJarPath+ " weka.core.converters.CSVSaver -i " + modelDir + testPrefix + "no-" + thresholdOutputFilename + " -o " + modelDir + testPrefix + "no-" + thresholdOutputFilenameCSV + " -F ,")
	
	yesResult = findResult(modelDir + testPrefix + "yes-" + thresholdOutputFilenameCSV, maxThreshold)
	noResult = findResult(modelDir + testPrefix + "no-" + thresholdOutputFilenameCSV, noThreshold)

	nbTrue = float(yesResult[0]) + float(yesResult[3])
	nbFalse = float(yesResult[1]) + float(yesResult[2])
	errorRate = nbFalse / (nbTrue + nbFalse)
	print("Yes - FMeasure => " + yesResult[9] + " | Taux d'erreur => " + str(errorRate * 100) + "%")
	print("No - FMeasure => " + noResult[9])

def calculPerformance(predictionFilename):
	f = open(predictionFilename, 'rb')
	reader = csv.reader(f, delimiter=',')
	rowSaved = []
	mesure = 0
	reader.next()
	for row in reader:
		if(float(row[9]) > mesure):
			mesure = float(row[9])
			rowSaved = row
	return rowSaved

def findResult(thresholdFilename, threshold):
	f = open(thresholdFilename, 'rb')
	reader = csv.reader(f, delimiter=',')
	rowSaved = []
	mesure = 0
	reader.next()
	for row in reader:
		if(float(row[12]) == threshold):
			return row
		if(float(row[12]) > threshold):
			return lastRow
		lastRow = row
	return None

# ----- MAIN ----- #
def main ():
	corpus = "data/KTFGHU14.csv"
	prep1_trainFilename = "data/KTFGHU14_train.arff"
	prep1_devFilename = "data/KTFGHU14_dev.arff"
	prep1_testFilename = "data/KTFGHU14_test.arff"

	preparation1(corpus, prep1_trainFilename, prep1_devFilename, prep1_testFilename)
	model1(prep1_trainFilename, prep1_devFilename, prep1_testFilename, "models/model1/", "44")
	model2(prep1_trainFilename, prep1_devFilename, prep1_testFilename, "models/model2/", "44")


main()
