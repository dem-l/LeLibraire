import subprocess 
import sys 
import os 


retvalue = os.system("java -cp lib/weka.jar weka.core.converters.CSVLoader " + sys.argv[1] + " -B 10000 > " + sys.argv[2]) 

print("Done: create file  | " + sys.argv[2] + " | from " + sys.argv[1]);

