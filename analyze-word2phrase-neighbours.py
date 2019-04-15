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

# returns P(word1|word2,dir,adj)
# dir is '<' if word1 left of word2, '>' if word1 right of word2
# corpus contains lists of sentences which are lists of words
def findCondProb(set1,set2,pos1,pos2,direction,wordDist,corpus):
	[set1Freq,set2Freq,totalWords,set1set2Freq,set1Index,set2Index] = [0,0,0,0,0,0]
	sentNum = 0
	elem1Len = len(set1[0].split())
	elem2Len = len(set2[0].split())

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		set1Freq += listCount(set1,sentence)
		set2Freq += listCount(set2,sentence)
		totalWords += len(sentence)

		while listCount(set2,sentence[startIndex:]) > 0:
			set2Index = startIndex + listIndex(set2,sentence[startIndex:])
			if direction == '>':
				set1Index = set2Index + elem2Len - 1 + wordDist
				if set1Index < len(sentence) - elem1Len + 1:
					if ' '.join(sentence[set1Index:set1Index+elem1Len]) in set1:
						set1set2Freq += 1
			elif direction == '<':
				set1Index = set2Index - wordDist - elem1Len + 1
				if set1Index >= 0:
					if ' '.join(sentence[set1Index:set1Index+elem1Len]) in set1:
						set1set2Freq += 1
			startIndex = set2Index + 1

	#sys.stderr.write('set1: ' + repr(set1Freq) + '\n')
	#sys.stderr.write('set2: ' + repr(set2Freq) + '\n')
	#sys.stderr.write('set1set2Freq: ' + repr(set1set2Freq) + '\n')
	#sys.stderr.write('totalWords: ' + repr(totalWords) + '\n')

	return (pos1,pos2,set1Freq,set2Freq,set1set2Freq,1.0*set1set2Freq/set2Freq,1.0*set1Freq/totalWords,1.0*set1set2Freq*totalWords/(set1Freq*set2Freq))


[sentFN,parseFN,wordNeighFN,phraseNeighFN,corpusFN] = sys.argv[1:6]

splitCorpus = []
neighbours = {}
word2phrase = {}
phrases = {}
WORD_THRESHOLD = 0.95
PHRASE_THRESHOLD = 30.0

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
	headword = ''
	for line in wordNeighFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1 and splitLine[0] != '' and splitLine[0][-1] == ':': 
			headword = splitLine[0][0:-1]
			sys.stderr.write('headword: ' + headword + '\n')
			neighbours[headword] = []
		elif len(splitLine) == 2:
			[word,score] = splitLine
			if float(score) <= WORD_THRESHOLD:
				neighbours[headword].append(word)

with open(phraseNeighFN) as phraseNeighFile:
	headPhrase = ''
	for line in phraseNeighFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1 and splitLine[0] != '' and splitLine[0][-1] == ':': 
			headPhrase = splitLine[0][0:-1]
			sys.stderr.write('headPhrase: ' + headPhrase + '\n')
			neighbours[headPhrase] = []
		elif len(splitLine) == 2:
			[phrase,score] = splitLine
			if float(score) <= PHRASE_THRESHOLD:
				neighbours[headPhrase].append(phrase)

# word-to-word conditonal probabilities
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
				dir1 = word2phrase[('neigh('+word+')','neigh('+phrase+')','<',k)] = findCondProb(neighbours[word],neighbours[phrase],i,span[0],'<',k,splitCorpus)
				dir2 = word2phrase[('neigh('+phrase+')','neigh('+word+')','>',k)] = findCondProb(neighbours[phrase],neighbours[word],span[0],i,'>',k,splitCorpus)
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
				dir1 = word2phrase[('neigh('+word+')','neigh('+phrase+')','>',k)] = findCondProb(neighbours[word],neighbours[phrase],i,span[0],'>',k,splitCorpus)
				dir2 = word2phrase[('neigh('+phrase+')','neigh('+word+')','<',k)] = findCondProb(neighbours[phrase],neighbours[word],span[0],i,'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

sys.stderr.write(sentence + '\n\n')
for k in sorted(word2phrase.keys(), key=operator.itemgetter(0,1,2,3)):
    sys.stderr.write('word2phrase' + repr(k) + '\t' + repr(word2phrase[k]) + '\n')

sortedPhrases = sorted(phrases.iteritems(), key=operator.itemgetter(0))
sys.stdout.write('\t' + '\t'.join(['neigh('+p[1]+')' for p in sortedPhrases]) + '\n')
for i in range(0,len(splitSentence)):
	word = splitSentence[i]
	sys.stdout.write('neigh('+splitSentence[i]+')' + '\t')
	for span,phrase in sortedPhrases:
		if i in range(span[0],span[1]): sys.stdout.write('--')
		else:
			direction = '<'
			dist = span[0] - i
			if i >= span[1]:
				direction = '>'
				dist = i - span[1] + 1
			if ('neigh('+word+')','neigh('+phrase+')',direction,dist) in word2phrase:
				sys.stdout.write(repr(word2phrase[('neigh('+word+')','neigh('+phrase+')',direction,dist)][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
