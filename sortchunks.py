import operator, sys

chunksFile = open(sys.argv[1])
chunkFreqs = {}

for line in chunksFile:
	splitLine = line.strip().split('\t')
	if len(splitLine) >= 2:
		chunkFreqs[splitLine[0]] = int(splitLine[1])

for k, v in sorted(chunkFreqs.items(), key=operator.itemgetter(1), reverse=True):
	print k + '\t' + repr(v)
