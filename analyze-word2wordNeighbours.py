import operator, sys

# order of words in list is from most to least similar to headword
def insertNeigh(headword, neighbour, dic):
	if headword not in dic:
		dic[headword] = []
	dic[headword].append(neighbour)

	return

def groupCount(neighbourhood,sentence):
	count = 0
	for word in sentence:
		if word in neighbourhood:
			count += 1

	return count

def groupIndex(neighbourhood,sentence):
	for i in range(len(sentence)):
		if sentence[i] in neighbourhood:
			return i

	raise ValueError

def listCount(neighbourhood,sentence):
	elemLen = len(neighbourhood[0].split())
	if elemLen == 1: return groupCount(neighbourhood,sentence)

	count = 0
	for i in range(0,len(sentence)-elemLen+1):
		if ' '.join(sentence[i:i+elemLen]) in neighbourhood:
			count += 1

	return count

def listIndex(neighbourhood,sentence):
	elemLen = len(neighbourhood[0].split())
	if elemLen == 1: return groupIndex(neighbourhood,sentence)

	for i in range(0,len(sentence)-elemLen+1):
		if ' '.join(sentence[i:i+elemLen]) in neighbourhood: return i

	raise ValueError

# elem1 and elem2 can be either a list containing just one word, or a list of phrasal neighbours
# returns P(word|neigh(phrase),dir,dist) or P(neigh(phrase)|word,dir,dist)
# dir is '<' if predicted element left of given element, '>' otherwise
# corpus contains lists of sentences which are lists of words
def findCondProb(elem1,elem2,pos1,pos2,direction,elemDist,corpus):
	[elem1Freq,elem2Freq,totalWords,elem1elem2Freq,elem1Index,elem2Index] = [0,0,0,0,0,0]
	sentNum = 0
	elem1Len = len(elem1[0].split())
	elem2Len = len(elem2[0].split())

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		elem1Freq += listCount(elem1,sentence)
		elem2Freq += listCount(elem2,sentence)
		totalWords += len(sentence)

		while listCount(elem2,sentence[startIndex:]) > 0:
			elem2Index = startIndex + listIndex(elem2,sentence[startIndex:])
			if direction == '>':
				elem1Index = elem2Index + elem2Len - 1 + elemDist
				if elem1Index < len(sentence) - elem1Len + 1:
					if ' '.join(sentence[elem1Index:elem1Index+elem1Len]) in elem1:
						elem1elem2Freq += 1
			elif direction == '<':
				elem1Index = elem2Index - elemDist - elem1Len + 1
				if elem1Index >= 0:
					if ' '.join(sentence[elem1Index:elem1Index+elem1Len]) in elem1:
						elem1elem2Freq += 1
			startIndex = elem2Index + 1

	sys.stderr.write('elem1Freq: ' + repr(elem1Freq) + '\n')
	sys.stderr.write('elem2Freq: ' + repr(elem2Freq) + '\n')
	sys.stderr.write('wordPhraseSetFreq: ' + repr(elem1elem2Freq) + '\n')

	return (pos1,pos2,elem1Freq,elem2Freq,elem1elem2Freq,1.0*elem1elem2Freq/elem2Freq,1.0*elem1Freq/totalWords,1.0*elem1elem2Freq*totalWords/(elem1Freq*elem2Freq))


[sentFN,neighFN,corpusFN] = sys.argv[1:4]

splitCorpus = []
neighbours = {}
word2wordNeigh = {}
WORD_THRESHOLD = 0.95

sentence = ''
with open(sentFN) as sentFile:
	sentence = sentFile.readline().lower().strip()
splitSentence = sentence.split()

with open(corpusFN) as corpusFile:
	for line in corpusFile:
		splitLine = line.strip().lower().split()
		splitCorpus.append(splitLine)

with open(neighFN) as neighFile:
	headWord = ''
	for line in neighFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1 and splitLine[0] != '' and splitLine[0][-1] == ':': 
			headWord = splitLine[0][0:-1]
			sys.stderr.write('headWord: ' + headWord + '\n')
			neighbours[headWord] = []
		elif len(splitLine) == 2:
			[word,score] = splitLine
			if float(score) <= WORD_THRESHOLD:
				neighbours[headWord].append(word)

splitSentence = sentence.split()
for i in range(0,len(splitSentence)):
	word1 = splitSentence[i]
	sys.stderr.write('word1: ' + word1 + '\n')
	for j in range(0,len(splitSentence)):
		word2 = splitSentence[j]
		sys.stderr.write('word2: ' + word2 + '\n')
		if i < j:
			wordDist = j - i
			for k in range(1,wordDist+1):
				dir1 = word2wordNeigh[(word1,'neigh('+word2+')','<',k)] = findCondProb([word1],neighbours[word2],i,j,'<',k,splitCorpus)
				dir2 = word2wordNeigh[('neigh('+word2+')',word1,'>',k)] = findCondProb(neighbours[word2],[word1],j,i,'>',k,splitCorpus)
				threshold = 0.0
				# compare the maximum value of the two directions to the threshold
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break
		elif i > j:
			wordDist = i - j
			for k in range(1,wordDist+1):
				dir1 = word2wordNeigh[(word1,'neigh('+word2+')','>',k)] = findCondProb([word1],neighbours[word2],i,j,'>',k,splitCorpus)
				dir2 = word2wordNeigh[('neigh('+word2+')',word1,'<',k)] = findCondProb(neighbours[word2],[word1],j,i,'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

sys.stderr.write(sentence + '\n\n')
for k in sorted(word2wordNeigh.keys(), key=operator.itemgetter(0,1,2,3)):
    sys.stderr.write('word2wordNeigh' + repr(k) + '\t' + repr(word2wordNeigh[k]) + '\n')

sys.stdout.write('\t' + '\t'.join(['neigh('+w+')' for w in splitSentence]) + '\n')
for i in range(0,len(splitSentence)):
	word1 = splitSentence[i]
	sys.stdout.write(word1 + '\t')
	for j in range(0,len(splitSentence)):
		if i == j: sys.stdout.write('--')
		else:
			word2 = splitSentence[j]
			direction = '<'
			if i > j:
				direction = '>'
			dist = abs(i-j)
			params = (word1,'neigh('+word2+')',direction,dist)
			if params in word2wordNeigh:
				sys.stdout.write(repr(word2wordNeigh[params][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
