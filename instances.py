import os
import sys
command = 'java -cp lib/weka.jar weka.core.Instances donnees1.arff'
if len(sys.argv) > 1:
	command = command + ' > ' + sys.argv[1]

os.system(command)