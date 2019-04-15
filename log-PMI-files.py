import math, sys

def isNumber(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

pmiFileName = sys.argv[1]

logValues = []
numOfWords = 0
firstLine = True
pruneTables = [0,2,3,5]
tableIndex = 0
table = []

with open(pmiFileName) as pmiFile:
	for line in pmiFile:
		splitLine = line.rstrip().split('\t')
		newSplitLine = []
		if splitLine == ['']:
			table = []
			tableIndex += 1
			continue
		if firstLine:
			numOfWords = len(splitLine) - 1
			firstLine = False
		table.append(splitLine)
		for col in range(len(splitLine)):
			row = len(table)-1
			entry = splitLine[col]
			entryIsNum = isNumber(entry)
			if entryIsNum:
				if tableIndex in pruneTables and col < row:
					entry = ''
				else:
					value = float(entry)
					if value > 1.0:
						logValue = math.log(value,2)
						#sys.stderr.write(repr(logValue) + '\n')
						logValues.append(logValue)
						entry = repr(logValue)
					else:
						entry = ''
			newSplitLine.append(entry)
		sys.stdout.write('\t'.join(newSplitLine) + '\n')

sumOfValues = sum(logValues)
sys.stdout.write('\n' + repr(sumOfValues) + '\n')
sys.stdout.write(repr(numOfWords) + '\n')
sys.stdout.write(repr(sumOfValues/numOfWords*1.0) + '\n')
