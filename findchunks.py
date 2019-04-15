import string, sys

def findAll(item, itemsList):
	itemsIndices = set([])
	tempList = itemsList
	base = 0
	while tempList.count(item) > 0:
		lowestIndex = tempList.index(item)
		itemsIndices.add(base + lowestIndex)
		tempList = tempList[lowestIndex+1:]
		base += lowestIndex + 1

	return itemsIndices

textFile = open(sys.argv[1])
textFileString = textFile.read()
splitTextFileString = textFileString.lower().split()
textFile.close()

vocab = set([])

sys.stderr.write('reading in vocab . . . ')
for word in splitTextFileString:
	if word not in vocab:
		vocab.add(word)
sys.stderr.write('done.\n')
sys.stderr.write('vocab size: ' + repr(len(vocab)) + '\n')

wordCount = 0
for word in vocab:
	wordCount += 1
	if wordCount % 10 == 0:
		sys.stderr.write(repr(wordCount) + '\n')
		sys.stderr.flush()
	#sys.stdout.write(word + '\n')
	wordIndices = findAll(word, splitTextFileString)
	#sys.stdout.write('occurrences found: ' + repr(len(wordIndices)) + '\n')
	firstSeenSeqIndices = {}
	repeatedSequences = {}
	sequenceLength = 1
	extend = True
	while extend:
		sequenceLength += 1
		extendableWordIndices = set([])
		extend = False
		for index in wordIndices:
			if index + sequenceLength > len(splitTextFileString):
				continue
			joinedCurrentSeq = ' '.join(splitTextFileString[index:index+sequenceLength])
			#sys.stdout.write(joinedCurrentSeq + ' . . . ')
			if joinedCurrentSeq not in firstSeenSeqIndices:
				#sys.stdout.write('new; ')
				#sys.stdout.write('index: ' + repr(index) + '\n')
				firstSeenSeqIndices[joinedCurrentSeq] = index
			else:
				if firstSeenSeqIndices[joinedCurrentSeq] not in extendableWordIndices:
					extendableWordIndices.add(firstSeenSeqIndices[joinedCurrentSeq])
				extendableWordIndices.add(index)
				#sys.stdout.write('extendableWordIndices: ' + repr(extendableWordIndices) + '\n')

				if joinedCurrentSeq not in repeatedSequences:
					repeatedSequences[joinedCurrentSeq] = 2
				else:
					repeatedSequences[joinedCurrentSeq] += 1
				#sys.stdout.write('seen; ')
				#sys.stdout.write('index: ' + repr(index) + '\n')
				#sys.stdout.write('frequency: ' + repr(repeatedSequences[word][joinedCurrentSeq]) + '\n')
				extend = True
		wordIndices = extendableWordIndices

	print word + ':'
	for seq in repeatedSequences:
		print seq + '\t' + repr(repeatedSequences[seq])
	sys.stdout.flush()
