# fixed inconsistency with 'direction' parameter
# from here on,
# '<' and '>' point towards the given
# e.g. "the park", "park" as the given, "the" as the predicted: direction is '>'

import sys, getNeighboursLib

START = '<START>'
END = '<END>'

def insertDic(word, neighbour, dic):
	if word not in dic:
		dic[word] = {neighbour: 1}
	else:
		if neighbour not in dic[word]:
			dic[word][neighbour] = 1
		else:
			dic[word][neighbour] += 1
	return		

def countNeighbours(text):
	neighbourDic = {}
	neighbourDic['<'] = {}
	neighbourDic['>'] = {}
	for line in text:
		for i in range(len(line)):
			word = line[i]
			neighbour = ''

			# look left
			if i > 0:
				neighbour = line[i-1]
			else:
				neighbour = START
				insertDic(neighbour, word, neighbourDic['>'])
			insertDic(word, neighbour, neighbourDic['<'])

			# look right
			if i < len(line)-1:
				neighbour = line[i+1]
			else:
				neighbour = END
				insertDic(neighbour, word, neighbourDic['<'])
			insertDic(word, neighbour, neighbourDic['>'])

	return

def getCondProb(predictedCluster, givenCluster, direction, neighbourDic):
	freqOfGiven = 0.0
	freqOfBoth = 0.0
	if direction == '<':
		# opposite directions, because word is the given
		for word in givenCluster:
			freqOfGiven += sum(neighbourDic['>'][word].values())
			freqOfBoth += sum(neighbourDic['>'][word][w2] for w2 in predictedCluster if w2 in neighbourDic['>'][word].keys())

	if direction == '>':
		for word in givenCluster:
			freqOfGiven += sum(neighbourDic['<'][word].values())
			freqOfBoth += sum(neighbourDic['<'][word][w2] for w2 in predictedCluster if w2 in neighbourDic['<'][word].keys())
	
	return 1.0 * freqOfBoth / freqOfGiven
	

textFilename = sys.argv[1]
jdFilename = sys.argv[2]

textLines = []
jd = {}
clusters = {} # caches top-n cluster by word
condProbs = {} # caches conditional probabilities
n = 5

sys.stderr.write('reading in text file . . . ')
# read in text
with open(textFilename) as textFile:
	for line in textFile:
		textLines.append(line.lower().strip().split())
textFile.close()
sys.stderr.write('done.\n')

sys.stderr.write('reading in Jaccard distances file . . . ')
jd = getNeighboursLib.getJD(jdFilename)
sys.stderr.write('done.\n')

sys.stderr.write('counting neighbours . . . ')
neighbourDic = countNeighbours(textLines)
sys.stderr.write('done.\n')

i = 0
for line in textLines:
	i += 1
	if i % 100 == 0:
		sys.stderr.write(repr(i) + ', ')

	for wordIndex in range(len(line)):
		predictedWord = line[wordIndex]
		predictedWordCluster = getNeighboursLib.getClusterWithCache(predictedWord, jd, n, clusters)
		if predictedWordCluster == None: continue

		# look left
		if wordIndex > 0:
			givenWord = line[wordIndex-1]
			givenWordCluster = getNeighboursLib.getClusterWithCache(givenWord, jd, n, clusters)
			if givenWordCluster == None: continue
			condProbs[(predictedWord, givenWord, '<')] = getCondProb(predictedWordCluster, givenWordCluster, '<', neighbourDic)
		else:
			givenWord = START
			givenWordCluster = set([givenWord])
			condProbs[(predictedWord, givenWord, '<')] = getCondProb(predictedWordCluster, givenWordCluster, '<', neighbourDic)	
			
		# look right
		if wordIndex < len(line)-1:
			givenWord = line[wordIndex+1]
			givenWordCluster = getNeighboursLib.getClusterWithCache(givenWord, jd, n, clusters)
			if givenWordCluster == None: continue
			condProbs[(predictedWord, givenWord, '>')] = getCondProb(predictedWordCluster, givenWordCluster, '>', neighbourDic)
		else:
			givenWord = END
			givenWordCluster = set([givenWord])
			condProbs[(predictedWord, givenWord, '>')] = getCondProb(predictedWordCluster, givenWordCluster, '>', neighbourDic)	

sys.stderr.write('\n')
sys.stderr.write('sorting and printing conditional probabilities . . . ')
# print out conditional probabilities
for condProbKey in sorted(condProbs, key=condProbs.__getitem__, reverse=True):
	sys.stdout.write(repr(condProbKey) + '\t' + repr(condProbs[condProbKey]) + '\n')
sys.stdout.write('\n')
sys.stderr.write('done.\n')

# print out clusters
sys.stderr.write('printing word clusters. . . ')
for word in clusters:
	sys.stdout.write(word + ': ' + ', '.join(clusters[word]) + '\n')
sys.stderr.write('done.\n')
