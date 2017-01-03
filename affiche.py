import arff
data=arff.load('data/donnees.arff')
i=1
for row in data:
	if i<=5:
		if row:
			print(row)
			i=i+1

