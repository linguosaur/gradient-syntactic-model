import codecs, math, operator, sys


def addToDictionary(item, dictionary):
	if item in dictionary:
		dictionary[item] += 1
	else:
		dictionary[item] = 1


textfile = codecs.open(sys.argv[1], encoding='latin-1')
text = textfile.readlines()

freqs = {}
freqsfile = codecs.open(sys.argv[2], encoding='latin-1')
for line in freqsfile:
	splitLine = line.strip().split('\t')
	if len(splitLine) == 2:
		freqs[splitLine[0]] = int(splitLine[1])

leftNeighbours = {}
rightNeighbours = {}

root = 'sodan'
for line in text:
	splitLine = line.strip().split()
	for word_i in range(len(splitLine)):
		if splitLine[word_i] == root:
			if word_i > 0:
				addToDictionary(splitLine[word_i-1], leftNeighbours)
			else:
				addToDictionary('^', leftNeighbours)
			if word_i < len(splitLine)-1:
				addToDictionary(splitLine[word_i+1], rightNeighbours)
			else:
				addToDictionary('$', rightNeighbours)

print root.encode('latin-1')
print
print 'left neighbours'
print
for w in sorted(leftNeighbours.iterkeys(), key=leftNeighbours.get, reverse=True):
	print w.encode('latin-1') + '\t' + repr(freqs[w]) + '\t' + repr(leftNeighbours[w]) + '\t' + repr(math.log(freqs[w]*leftNeighbours[w]))
print
print 'right neighbours'
print
for w in sorted(rightNeighbours.iterkeys(), key=rightNeighbours.get, reverse=True):
	print w.encode('latin-1') + '\t' + repr(freqs[w]) + '\t' + repr(rightNeighbours[w]) + '\t' + repr(math.log(freqs[w]*rightNeighbours[w]))

