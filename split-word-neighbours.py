import sys

allSentsFileName = sys.argv[1]
neighboursBatchFileName = sys.argv[2]

allSents = []
allScores = {}
with open(allSentsFileName) as sentsFile:
	for line in sentsFile:
		if line.strip() != '':
			splitSent = line.strip().split()
			allSents.append(splitSent)

with open(neighboursBatchFileName) as neighboursBatchFile:
	headElem = ''
	for line in neighboursBatchFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1:
			if splitLine[0] != '' and splitLine[0][-1] == ':':
				headElem = splitLine[0][0:-1]
				allScores[headElem] = {}
				sys.stderr.write('head element: ' + headElem + '\n')
		elif len(splitLine) == 2:
			[neighbour,score] = splitLine
			allScores[headElem][neighbour] = score

sys.stderr.write('number of head elements: ' + repr(len(allScores)) + '\n')

index = 2
notIndices = [2]
outFileNameHead = '/home/simonmin/output/sent'
outFileNameTail = '-neighbours-words.txt'
for sent in allSents:
	if index in notIndices:
		index += 1
		continue
	outFileName = outFileNameHead + repr(index) + outFileNameTail
	with open(outFileName,'w') as outFile:
		for headElem in sent:
			outFile.write(headElem + ':\n')
			for neighbour in allScores[headElem]:
				outFile.write(neighbour + '\t' + allScores[headElem][neighbour] + '\n')
			outFile.write('\n')
	index += 1
