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

			if i > 0:
				neighbour = line[i-1]
			else:
				neighbour = '<START>'
			insertDic(word, neighbour, neighbourDic['left'])

			if i < len(line)-1:
				neighbour = line[i+1]
			else:
				neighbour = '<STOP>'
			insertDic(word, neighbour, neighbourDic['right'])

def calcCondProb(neighbourDic):
	for word in neighbourDic['left']:
		

posFilename = sys.argv[1]

posLines = []
neighbourDic = {}
condProbs = {} # caches conditional probabilities

sys.stderr.write('reading in text file . . . ')
# read in text
with open(posFilename) as posFile:
	for line in posFile:
		posLines.append(line.strip().split())
posFile.close()
sys.stderr.write('done.\n')

sys.stderr.write('counting neighbours . . . ')
countNeighbours(posLines, neighbourDic)
sys.stderr.write('done.\n')

sys.stderr.write('generating conditional probabilities . . . ')
calcCondProbs(neighbourDic)
sys.stderr.write('done.\n')

i = 0
for line in posLines:
	i += 1
	if i % 100 == 0:
		sys.stderr.write(repr(i) + ', ')

	for wordIndex in range(len(line)):
		givenWord = line[wordIndex]

		# look left
		if wordIndex > 0:
			predictedWord = line[wordIndex-1]
			condProbs[(predictedWord, givenWord, '<')] = getCondProb(predictedWord, givenWord, '<', neighbourDic)
			
		# look right
		if wordIndex < len(line)-1:
			predictedWord = line[wordIndex+1]
			condProbs[(predictedWord, givenWord, '>')] = getCondProb(predictedWord, givenWord, '>', neighbourDic)

sys.stderr.write('\n')
sys.stderr.write('sorting and printing conditional probabilities . . . ')
# print out conditional probabilities
for condProbKey in sorted(condProbs, key=condProbs.__getitem__, reverse=True):
	sys.stdout.write(repr(condProbKey) + '\t' + repr(condProbs[condProbKey]) + '\n')
sys.stdout.write('\n')
sys.stderr.write('done.\n')
