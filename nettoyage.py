import csv

filename='data/donnees.csv'
filename1='data/donnees1.csv'

f = open(filename, 'rb')
f1 = open(filename1, 'wb')

reader = csv.reader(f, delimiter=',')
writer = csv.writer(f1)

writer.writerow (reader.next())

for row in reader:
	if row[2] != 'NA' and row[5] != 'NA':
		writer.writerow (row)