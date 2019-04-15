import sys, getNeighboursLib


def insertDic(word, neighbour, dic):
	if word not in dic:
		dic[word] = {neighbour: 1}
	else:
		if neighbour not in dic[word]:
			dic[word][neighbour] = 1
		else:
			dic[word][neighbour] += 1
	return		

def countNeighbours(text, neighbourDic):
	neighbourDic['left'] = {}
	neighbourDic['right'] = {}
	for line in text:
		for i in range(len(line)):
			word = line[i]
			neighbour = ''
			if i < len(line)-1:
				neighbour = line[i+1]
			else:
				neighbour = '$'
			insertDic(word, neighbour, neighbourDic['left'])

			if i > 0:
				neighbour = line[i-1]
			else:
				neighbour = '^'
			insertDic(word, neighbour, neighbourDic['right'])
	return

def getCondProb(predictedCluster, givenCluster, direction, neighbourDic):
	pairsWithGiven = []

	freqOfGiven = 0.0
	freqOfBoth = 0.0
	if '<' in direction:
		for word in givenCluster:
			freqOfGiven += sum(neighbourDic['left'][word].values())
			freqOfBoth += sum(neighbourDic['left'][word][w2] for w2 in predictedCluster if w2 in neighbourDic['left'][word].keys())

	if '>' in direction:
		for word in givenCluster:
			freqOfGiven += sum(neighbourDic['right'][word].values())
			freqOfBoth += sum(neighbourDic['right'][word][w2] for w2 in predictedCluster if w2 in neighbourDic['right'][word].keys())
	
	return 1.0 * freqOfBoth / freqOfGiven
	

textFilename = sys.argv[1]
jdFilename = sys.argv[2]

textLines = []
jd = {}
neighbourDic = {}
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
countNeighbours(textLines, neighbourDic)
sys.stderr.write('done.\n')

i = 0
for line in textLines:
	i += 1
	if i % 100 == 0:
		sys.stderr.write(repr(i) + ', ')

	for wordIndex in range(len(line)):
		givenWord = line[wordIndex]
		givenWordCluster = getNeighboursLib.getClusterWithCache(givenWord, jd, n, clusters)
		if givenWordCluster == None: continue

		# look left
		if wordIndex > 0:
			predictedWord = line[wordIndex-1]
			predictedWordCluster = getNeighboursLib.getClusterWithCache(predictedWord, jd, n, clusters)
			if predictedWordCluster == None: continue
			condProbs[(predictedWord, givenWord, '<')] = getCondProb(predictedWordCluster, givenWordCluster, '<', neighbourDic)
			
		# look right
		if wordIndex < len(line)-1:
			predictedWord = line[wordIndex+1]
			predictedWordCluster = getNeighboursLib.getClusterWithCache(predictedWord, jd, n, clusters)
			if predictedWordCluster == None: continue
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
