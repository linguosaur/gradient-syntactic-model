import re, sys
from random import shuffle

sentFileName = sys.argv[1]
outFileNameHead = '/home/simonmin/output/sent'
outFileNameTail = '.txt'

with open(sentFileName) as sentFile:
	index = 2
	for line in sentFile:
		splitLine = line.split()
		splitLine2 = [x.lower() for x in splitLine if re.search('[A-Za-z0-9\']+', x) != None]
		outFileName = outFileNameHead + repr(index) + outFileNameTail
		#sys.stdout.write(' '.join(splitLine2) + '\n')
		with open(outFileName, 'w') as outFile:
			outFile.write(' '.join(splitLine2) + '\n')
		index += 1
		outFileName = outFileNameHead + repr(index) + outFileNameTail
		shuffledLine = shuffle(splitLine2)
		#sys.stdout.write(' '.join(splitLine2) + '\n\n')
		with open(outFileName, 'w') as outFile:
			outFile.write(' '.join(splitLine2) + '\n')
		index += 1
