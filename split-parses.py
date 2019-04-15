import sys

allParsesFileName = sys.argv[1]

allSents = {}
allPhrases = {}
with open(allParsesFileName) as parsesFile:
	index = 1 # first sentence is sent2
	sent = ''
	for line in parsesFile:
		if line.strip() != '':
			splitLine = line.strip().split('\t')
			if len(splitLine) == 1:
				index += 1
				allSents[index] = splitLine[0]
				allPhrases[index] = []
			elif len(splitLine) == 3:
				allPhrases[index].append(splitLine)

notIndices = [2]
outFileNameHead = '/home/simonmin/output/sent'
outFileNameTail = '-parse.txt'
for index in allSents:
	if index in notIndices:
		continue
	outFileName = outFileNameHead + repr(index) + outFileNameTail
	with open(outFileName,'w') as outFile:
		outFile.write(allSents[index] + '\n')
		for phraseInfo in allPhrases[index]:
			outFile.write('\t'.join(phraseInfo) + '\n')
