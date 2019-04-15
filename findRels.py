import operator, re, string, sys


def getCollab(w2c, contextWords):
	collabs = {}
	for word in w2c:
		wordProfile = w2c[word]
		for pos in range(len(wordProfile)):
			cooccurences = set(contextWords) & set(wordProfile[pos].keys())
			if len(cooccurences) > 0:
			#if len(cooccurences) > len(contextWords) / 2:
				if word not in collabs:
					collabs[word] = []
					for i in range(len(wordProfile)):
						collabs[word].append({})
				for contextWord in cooccurences:
					collabs[word][pos][contextWord] = wordProfile[pos][contextWord]
	return collabs

def printCollab(w2c, contextWords):
	collaboration = getCollab(w2c, contextWords)
	for word in collaboration:
		print repr(word) 
		for pos in range(len(collaboration[word])):
			print 'pos: ' + repr(pos) + '\t' + repr(collaboration[word][pos])
	print

def initializeWordContexts(positions):
	wordContexts = []
	for k in range(positions*2):
		wordContexts.append({})
	return wordContexts

words2contexts = {}
freqs = {}
tokenFreq = 0

topList = []
bottomList = []
quota = 500

textFile = open(sys.argv[1])
textFileLines = textFile.readlines()
textFile.close()

contextLength = 1

words2contexts['^'] = initializeWordContexts(contextLength)
words2contexts['$'] = initializeWordContexts(contextLength)

for line in textFileLines:
	splitLine = line.lower().split()
	lineLength = len(splitLine)
	tokenFreq += lineLength

	if splitLine[0] in words2contexts['^'][1]:
		words2contexts['^'][1][splitLine[0]] += 1
	else:
		words2contexts['^'][1][splitLine[0]] = 1
	if splitLine[-1] in words2contexts['$'][0]:
		words2contexts['$'][0][splitLine[-1]] += 1
	else:
		words2contexts['$'][0][splitLine[-1]] = 1
	if '^' not in freqs:
		freqs['^'] = 1
	else:
		freqs['^'] += 1
	if '$' not in freqs:
		freqs['$'] = 1
	else:
		freqs['$'] += 1

	for i in range(lineLength):
		word = splitLine[i]

		if word not in freqs:
			freqs[word] = 1
		else:
			freqs[word] += 1

		if word not in words2contexts:
			words2contexts[word] = initializeWordContexts(contextLength)

		pos = 0
		for j in range(i-contextLength, i) + range(i+1, i+contextLength+1):
			if j >= 0 and j < lineLength:
				contextWord = splitLine[j]
			elif j < 0:
				contextWord = '^'
			else:
				contextWord = '$'

			if contextWord in words2contexts[word][pos]:
				words2contexts[word][pos][contextWord] += 1
			else:
				words2contexts[word][pos][contextWord] = 1
			pos += 1

# for each count, calculate how many times more frequent it is than expected, that the contextWord is in this position relative to the target word
for word in words2contexts:
	for pos in range(len(words2contexts[word])):
		for contextWord in words2contexts[word][pos]:
			words2contexts[word][pos][contextWord] *= 1.0 / ((1.0 * freqs[contextWord] / tokenFreq) * freqs[word])
#			freqRatio = words2contexts[word][pos][contextWord]

				# fill topList and bottomList
#				if len(topList) < quota:
#					topList.append((freqRatio, word, pos, contextWord))
#				elif len(topList) == quota and freqRatio > min(topList)[0]:
#					topList.remove(min(topList))
#					topList.append((freqRatio, word, pos, contextWord))
#				if len(bottomList) < quota:
#					bottomList.append((freqRatio, word, pos, contextWord))
#				elif len(bottomList) == quota and freqRatio < max(bottomList)[0]:
#					bottomList.remove(max(bottomList))
#					bottomList.append((freqRatio, word, pos, contextWord))

# print contexts and freqRatios
#for word in words2contexts:
#	sys.stdout.write(word + '\t')
#	for pos in range(len(words2contexts[word])):
#		sys.stdout.write(repr(pos) + '\t' + repr(words2contexts[word][pos]) + '\n')
#print

# show collaborations among a group of words
#collaboration = printCollab(words2contexts, ['he', 'she', 'we', 'they'])
#collaboration = printCollab(words2contexts, ['managed', 'just', 'switched', 'felt', 'still'])

#print 'top list'
#topList.sort()
#topList.reverse()
#for i in range(len(topList)):
#	print repr(i) + '\t' + repr(topList[i])
#print
#print 'bottom list'
#bottomList.sort()
#for i in range(len(bottomList)):
#	print repr(i) + '\t' + repr(bottomList[i])

# print out corpus, with freqRatios
for line in textFileLines:
	splitLine = line.lower().split()
	outputLine = []
	for i in range(len(splitLine)):
		word = splitLine[i]
		leftContext = ''
		if i == 0:
			leftContext = '^'
		else:
			leftContext = splitLine[i-1]

		if i < len(splitLine)-1:
			outputLine.extend([repr(words2contexts[word][0][leftContext]), word])
		else:
			outputLine.extend([repr(words2contexts[word][0][leftContext]), word, repr(words2contexts[word][1]['$'])])
	sys.stdout.write(' '.join(outputLine) + '\n')
