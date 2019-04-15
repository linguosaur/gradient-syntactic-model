import sys, math
from ast import literal_eval

def insertPOSLookupTable(word, pos, table):
	if word in table:
		table[word].add(pos)
	else:
		table[word] = set([pos])

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

def insert2DFreqTable(key1, key2, table):
	if key1 not in table:
		table[key1] = {key2: 1}
	elif key2 in table[key1]:
		table[key1][key2] += 1
	elif key2 not in table[key1]:
		table[key1][key2] = 1

def getWordFreqInPOS(wordFreq, posSet, posFreqs):
	setFreq = sum(posFreqs[pos] for pos in posSet)
	#sys.stderr.write('word: ' + word + '\tword freq: ' + wordFreq + '\tPOS set: ' + repr(posSet) + '\tset freq: ' + repr(setFreq) + '\n')

	return 1.0 * wordFreq / setFreq


depFilename = sys.argv[1]
condprobsFilename = sys.argv[2]

wordSentences = []
posSentences = []
wordFreqs = {}
posFreqs = {}
posLookup = {}

with open(depFilename) as depFile:
	wordSentence = []
	posSentence = []
	for line in depFile:
		splitline = line.strip().split('\t')
		if len(splitline) > 4:
			word = splitline[2]
			pos = splitline[3]
			wordSentence.append(word)
			posSentence.append(pos)
			insertFreqTable(word, wordFreqs)
			insertFreqTable(pos, posFreqs)
			insert2DFreqTable(word, pos, posLookup)
		else:
			wordSentences.append(wordSentence)
			posSentences.append(posSentence)
			wordSentence = []
			posSentence = []
depFile.close()

totalTokens = sum(wordFreqs.values())
sys.stderr.write('totalTokens: ' + repr(totalTokens) + '\n')
sys.stderr.write('len(wordSentences): ' + repr(len(wordSentences)) + '\n')
sys.stderr.write('len(posSentences): ' + repr(len(posSentences)) + '\n')

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

i = 0
for sentence_i in range(len(wordSentences)):
	wordSentence = wordSentences[sentence_i]
	posSentence = posSentences[sentence_i]
	for word_i in range(len(wordSentence)):
		predictedWord = wordSentence[word_i]
		predictedPOS = posSentence[word_i]
		givenPOS = ''
		qPrediction = 0.0

		if word_i > 0:
			givenWord = wordSentence[word_i-1]
			givenPOS = posSentence[word_i-1]
			qPrediction += left[predictedPOS][givenPOS]
		if word_i < len(wordSentence)-1:
			givenWord = wordSentence[word_i+1]
			givenPOS = posSentence[word_i+1]
			qPrediction += right[predictedPOS][givenPOS]

		p = 1.0 * wordFreqs[predictedWord] / totalTokens
		q = 0.0
		if qPrediction == 0.0:
			q = p
		else:
			qWordGivenPOS = getWordFreqInPOS(wordFreqs[predictedWord], posLookup[predictedWord], posFreqs)
			q = qWordGivenPOS * qPrediction
		selfInfo = -math.log(q, 2.0)
		entropy += p * selfInfo

sys.stdout.write('Cross Entropy: ' + repr(entropy) + ' bits \n')
sys.stdout.write('Cross Entropy per word: ' + repr(entropy/totalTokens) + ' bits \n')
sys.stdout.write('Perplexity per word: ' + repr(pow(2, entropy/totalTokens)) + '\n\n')
