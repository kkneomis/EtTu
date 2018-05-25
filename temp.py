import csv
import json

keys = []
values= []
with open('letterfreg.csv', 'rU') as f:
    spamreader = csv.reader(f, delimiter=',', quotechar='|')
    for row in spamreader:
        keys.append(row[0])
        values.append(float(row[1]))

print keys
print values
