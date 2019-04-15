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


[sentFN,parseFN,wordNeighFN,corpusFN] = sys.argv[1:5]

splitCorpus = []
neighbours = {}
phrase2wordNeigh = {}
phrases = {}
WORD_THRESHOLD = 0.95

sentence = ''
with open(sentFN) as sentFile:
	sentence = sentFile.readline().lower().strip()
splitSentence = sentence.split()

with open(corpusFN) as corpusFile:
	for line in corpusFile:
		splitLine = line.strip().lower().split()
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

with open(wordNeighFN) as wordNeighFile:
	headWord = ''
	for line in wordNeighFile:
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
	word = splitSentence[i]
	sys.stderr.write('word: ' + word + '\n')
	for span,phrase in phrases.iteritems():
		sys.stderr.write('phrase: ' + phrase + '\n')
		if i in range(span[0],span[1]): continue
		if i < span[0]:
			wordDist = span[0] - i
			for k in range(1,wordDist+1):
				dir1 = phrase2wordNeigh[('neigh('+word+')',phrase,'<',k)] = findCondProb(neighbours[word],[phrase],i,span[0],'<',k,splitCorpus)
				dir2 = phrase2wordNeigh[(phrase,'neigh('+word+')','>',k)] = findCondProb([phrase],neighbours[word],span[0],i,'>',k,splitCorpus)
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
				dir1 = phrase2wordNeigh[('neigh('+word+')',phrase,'>',k)] = findCondProb(neighbours[word],[phrase],i,span[0],'>',k,splitCorpus)
				dir2 = phrase2wordNeigh[(phrase,'neigh('+word+')','<',k)] = findCondProb([phrase],neighbours[word],span[0],i,'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

sys.stderr.write(sentence + '\n\n')
for k in sorted(phrase2wordNeigh.keys(), key=operator.itemgetter(0,1,2,3)):
    sys.stderr.write('phrase2wordNeigh' + repr(k) + '\t' + repr(phrase2wordNeigh[k]) + '\n')

sortedPhrases = sorted(phrases.iteritems(), key=operator.itemgetter(0))
sys.stdout.write('\t' + '\t'.join(['neigh('+w+')' for w in splitSentence]) + '\n')
for span,phrase in sortedPhrases:
	sys.stdout.write(phrase + '\t')
	for i in range(0,len(splitSentence)):
		word = splitSentence[i]
		if i in range(span[0],span[1]): sys.stdout.write('--')
		else:
			direction = '<'
			dist = span[0] - i
			if i >= span[1]:
				direction = '>'
				dist = i - span[1] + 1
			if ('neigh('+word+')',phrase,direction,dist) in phrase2wordNeigh:
				sys.stdout.write(repr(phrase2wordNeigh[('neigh('+word+')',phrase,direction,dist)][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
