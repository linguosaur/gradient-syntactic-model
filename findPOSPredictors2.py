# fixed inconsistency with 'direction' parameter
# from here on,
# '<' means that the given word is on the left of the predicted word, and vice versa
# e.g. "the park", "park" as the given, "the" as the predicted: direction is '>'

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

# caches conditional probabilities
def calcCondProb(neighbourDic):
	condprobs = {}
	for direction in neighbourDic:
		for word in neighbourDic[direction]:
			freqGiven = sum(neighbourDic[direction][word])
			for neighbour in neighbour[direction][word]:
				freqBoth = neighbour[direction][word][neighbour]
				condprobs[(neighbour, word, direction)] = 1.0 * freqBoth / freqGiven

	return condprobs

posFilename = sys.argv[1]

posLines = []
neighbourDic = {}
 
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
condProbs = calcCondProbs(neighbourDic)
sys.stderr.write('done.\n')

sys.stderr.write('\n')
sys.stderr.write('sorting and printing conditional probabilities . . . ')
# print out conditional probabilities
for condProbKey in sorted(condProbs, key=condProbs.__getitem__, reverse=True):
	sys.stdout.write(repr(condProbKey) + '\t' + repr(condProbs[condProbKey]) + '\n')
sys.stdout.write('\n')
sys.stderr.write('done.\n')
