import sys

profileFileName = sys.argv[1]
wordsFileName = sys.argv[2]

vocab = set([])
notFound = False
with open(profileFileName) as profileFile:
	for line in profileFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1 and splitLine[0] != '' and splitLine[0][-1] == ':':
			word = splitLine[0][0:-1]
			vocab.add(word)

with open(wordsFileName) as wordsFile:
	for line in wordsFile:
		splitLine = line.strip().split()
		for word in splitLine:
			if word not in vocab:
				sys.stderr.write(word + ' not found\n')
				notFound = True

if not notFound:
	sys.stderr.write('all words present in profile file\n')
