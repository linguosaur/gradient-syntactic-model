import operator, string, sys

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
repeatedSequences = {}
for word in vocab:
	wordCount += 1
	sys.stderr.write(repr(wordCount) + ', ')
	sys.stderr.flush()
	wordIndices = findAll(word, splitTextFileString)
	firstSeenSeqIndices = {}
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
			if joinedCurrentSeq not in firstSeenSeqIndices:
				firstSeenSeqIndices[joinedCurrentSeq] = index
			else:
				if firstSeenSeqIndices[joinedCurrentSeq] not in extendableWordIndices:
					extendableWordIndices.add(firstSeenSeqIndices[joinedCurrentSeq])
				extendableWordIndices.add(index)

				if joinedCurrentSeq not in repeatedSequences:
					repeatedSequences[joinedCurrentSeq] = 2
				else:
					repeatedSequences[joinedCurrentSeq] += 1
				extend = True
		wordIndices = extendableWordIndices

for seq, freq in sorted(repeatedSequences.items(), key=operator.itemgetter(1), reverse=True):
	sys.stdout.write(seq + '\t' + repr(freq) + '\n')
