import sys, math
from ast import literal_eval

def insertCondprobTable(predicted, given, condprob, table):
	if predicted not in table:
		table[predicted] = {given: condprob}
	else:
		table[predicted][given] = condprob

def insertFreqTable(word, table):
	if word not in table:
		table[word] = 1
	else:
		table[word] += 1

def getWordFreqInTopN(word, neighbours, freq):
	setFreq = sum([freq[w] for w in neighbours])
	wordFreq = freq[word]

	return 1.0 * wordFreq / (setFreq + wordFreq)

def getProbForClusterCombos(word, predictor, condprobTable):
	qPrediction = 0.0

	if word in condprobTable and predictor in condprobTable[word]:
		qPrediction += condprobTable[word][predictor]
	
	return qPrediction


textFilename = sys.argv[1]
condprobsFilename = sys.argv[2]
topNFilename = sys.argv[3]

sentences = []
freq = {}

with open(textFilename) as textFile:
	for line in textFile:
		splitline = line.lower().strip().split()
		for word in splitline:
			insertFreqTable(word, freq)
		sentences.append(splitline)
textFile.close()

totalTokens = sum(freq.values())

topN = {}

with open(topNFilename) as topNFile:
	for line in topNFile:
		splitline = line.strip().split(': ')
		headword = splitline[0]
		neighbours = set(splitline[1].split(', '))
		topN[headword] = neighbours
topNFile.close()

left = {}
right = {}

with open(condprobsFilename) as condprobsFile:
	for line in condprobsFile:
		splitline = line.strip().split('\t')
		(predicted, given, direction) = literal_eval(splitline[0])
		condprob = float(splitline[1])
		if direction == '<':
			insertCondprobTable(predicted, given, condprob, left)
		elif direction == '>':
			insertCondprobTable(predicted, given, condprob, right)
condprobsFile.close()

entropy = 0.0

for sentence in sentences:
	for word_i in range(len(sentence)):
		predicted = sentence[word_i]
		qPrediction = 0.0

		if word_i > 0:
			given = sentence[word_i-1]
			qPrediction += getProbForClusterCombos(predicted, given, left)
		if word_i < len(sentence)-1:
			given = sentence[word_i+1]
			qPrediction += getProbForClusterCombos(predicted, given, right)

		p = 1.0 * freq[predicted] / totalTokens
		q = 0.0
		if qPrediction == 0.0:
			q = p
		else:
			qWordGivenTopN = getWordFreqInTopN(predicted, topN[predicted], freq)
			q = qWordGivenTopN * qPrediction
		selfInfo = -math.log(q, 2.0)
		entropy += p * selfInfo

sys.stdout.write('Cross Entropy: ' + repr(entropy) + ' bits \n')
sys.stdout.write('Cross Entropy per word: ' + repr(entropy/totalTokens) + ' bits \n')
sys.stdout.write('Perplexity per word: ' + repr(pow(2, entropy/totalTokens)) + '\n\n')
