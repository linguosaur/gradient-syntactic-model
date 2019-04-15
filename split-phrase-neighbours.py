import sys

allParsesFileName = sys.argv[1]
neighboursBatchFileName = sys.argv[2]

allPhrases = {}
allScores = {}
with open(allParsesFileName) as parsesFile:
	index = 1 # first sentence is sent2
	for line in parsesFile:
		if line.strip() != '':
			splitLine = line.strip().split('\t')
			if len(splitLine) == 1:
				index += 1
				allPhrases[index] = []
			elif len(splitLine) == 3:
				allPhrases[index].append(splitLine[1])

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

notIndices = [2]
outFileNameHead = '/home/simonmin/output/sent'
outFileNameTail = '-neighbours-phrases.txt'
for index in allPhrases:
	if index in notIndices:
		continue
	outFileName = outFileNameHead + repr(index) + outFileNameTail
	with open(outFileName,'w') as outFile:
		for headPhrase in allPhrases[index]:
			outFile.write(headPhrase + ':\n')
			for neighbour in allScores[headPhrase]:
				outFile.write(neighbour + '\t' + allScores[headPhrase][neighbour] + '\n')
			outFile.write('\n')
