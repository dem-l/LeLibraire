import subprocess
p = subprocess.Popen(['java', '-cp \'lib/weka.jar\' weka.classifiers.Bayes.BayesNet -t data/KTFGHU14.arff'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

out, err = p.communicate()

print "[** OUPUT **]"
print out

print"[** ERROR **]"
print err

