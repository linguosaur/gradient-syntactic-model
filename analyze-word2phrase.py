import operator, sys

def countList(smallList,bigList):
	if len(smallList) == 1: return bigList.count(smallList[0])

	count = 0
	for i in range(0,len(bigList)-len(smallList)+1):
		match = True
		for j in range(0,len(smallList)):
			if bigList[i+j] != smallList[j]:
				match = False
				break
		if match: count += 1

	return count

def indexList(smallList,bigList):
	if len(smallList) == 1: return bigList.index(smallList[0])

	for i in range(0,len(bigList)-len(smallList)+1):
		match = True
		for j in range(0,len(smallList)):
			if bigList[i+j] != smallList[j]:
				match = False
				break
		if match: return i

	raise ValueError

# returns P(elem1|elem2,dir,adj),
# where elem1 and elem2 are lists of words
# dir is '<' if elem1 left of elem2, '>' if elem1 right of elem2
# corpus contains lists of sentences which are lists of elements
#
def findCondProb(elem1,elem2,pos1,pos2,direction,elemDist,corpus):
	[elem1Freq,elem2Freq,totalWords,elem1elem2Freq,elem1Index,elem2Index] = [0,0,0,0,0,0]
	sentNum = 0

	sys.stderr.write(repr(elem1) + '\t' + repr(elem2) + '\n')

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		elem1Freq += countList(elem1,sentence)
		elem2Freq += countList(elem2,sentence)
		totalWords += len(sentence)

		while countList(elem2,sentence[startIndex:]) > 0:
			elem2Index = startIndex + indexList(elem2,sentence[startIndex:])
			if direction == '>':
				elem1Index = elem2Index + len(elem2) - 1 + elemDist
				if elem1Index < len(sentence):
					if sentence[elem1Index:elem1Index+len(elem1)] == elem1:
						elem1elem2Freq += 1
			elif direction == '<':
				elem1Index = elem2Index - elemDist - len(elem1) + 1
				if elem1Index >= 0:
					if sentence[elem1Index:elem1Index+len(elem1)] == elem1:
						elem1elem2Freq += 1
			startIndex = elem2Index + 1

	sys.stderr.write(' '.join(elem1) + ': ' + repr(elem1Freq) + '\n')
	sys.stderr.write(' '.join(elem2) + ': ' + repr(elem2Freq) + '\n')
	sys.stderr.write('elem1elem2Freq: ' + repr(elem1elem2Freq) + '\n')

	return (pos1,pos2,elem1Freq,elem2Freq,elem1elem2Freq,1.0*elem1elem2Freq/elem2Freq,1.0*elem1Freq/totalWords,1.0*elem1elem2Freq*totalWords/(elem1Freq*elem2Freq))

[sentFN,parseFN,corpusFN] = sys.argv[1:4]

splitCorpus = []
word2phrase = {}
phrases = {}

sentence = ''
with open(sentFN) as sentFile:
	sentence = sentFile.readline().lower().strip()

with open(corpusFN) as corpusFile:
	for line in corpusFile:
		splitLine = line.lower().strip().split()
		splitCorpus.append(splitLine)

with open(parseFN) as parseFile:
	for line in parseFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) > 1:
			span = tuple(splitLine[0][1:-1].split(','))
			span = tuple([int(span[0]),int(span[1])])
			phrases[span] = splitLine[1]

for span,phrase in phrases.iteritems():
	sys.stderr.write('\t'.join([repr(span),phrase]) + '\n')

# word-to-phrase conditonal probabilities
splitSentence = sentence.split()
for i in range(0,len(splitSentence)):
	word = splitSentence[i]
	for span,phrase in phrases.iteritems():
		if i in range(span[0],span[1]): continue
		if i < span[0]:
			wordDist = span[0] - i
			for k in range(1,wordDist+1):
				dir1 = word2phrase[(word,phrase,'<',k)] = findCondProb([word],phrase.split(),i,span[0],'<',k,splitCorpus)
				dir2 = word2phrase[(phrase,word,'>',k)] = findCondProb(phrase.split(),[word],span[0],i,'>',k,splitCorpus)
				threshold = 0.0
				# compare the maximum value of the two directions to the threshold
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break
		else:
			wordDist = i - span[1] + 1
			for k in range(1,wordDist+1):
				dir1 = word2phrase[(word,phrase,'>',k)] = findCondProb([word],phrase.split(),i,span[0],'>',k,splitCorpus)
				dir2 = word2phrase[(phrase,word,'<',k)] = findCondProb(phrase.split(),[word],span[0],i,'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

sys.stderr.write(sentence + '\n\n')
for k,v in sorted(word2phrase.iteritems(), key=operator.itemgetter(1)):
    sys.stderr.write('word2phrase' + repr(k) + '\t' + repr(v) + '\n')

sortedPhrases = sorted(phrases.iteritems(), key=operator.itemgetter(0))
sys.stdout.write('\t' + '\t'.join([p[1] for p in sortedPhrases]) + '\n')
for i in range(0,len(splitSentence)):
	word = splitSentence[i]
	sys.stdout.write(word + '\t')
	for span,phrase in sortedPhrases:
		if i in range(span[0],span[1]): sys.stdout.write('--')
		else:
			direction = '<'
			dist = span[0] - i 
			if i >= span[1]:
				direction = '>'
				dist = i - span[1] + 1
			if (word,phrase,direction,dist) in word2phrase:
				sys.stdout.write(repr(word2phrase[(word,phrase,direction,dist)][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
