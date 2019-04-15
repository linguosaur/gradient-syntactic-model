import operator, sys


# span1 and span2 are 2-tuples
# start: index of first element; end: start + len(span)
# same format as Python range
def overlap(span1,span2):
	if len(set(range(span1[0],span1[1])) & set(range(span2[0],span2[1]))) == 0:
		return False

	return True

def dist(span1,span2):
	if overlap(span1,span2): return 0
	if span1[1] <= span2[0]:
		return span2[0] - span1[1] + 1

	return span2[1] - span1[0] - 1

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


[parseFN,phraseNeighFN,corpusFN] = sys.argv[1:4]

splitCorpus = []
neighbours = {}
phrase2phraseNeighbours = {}
phrases = {}
PHRASE_THRESHOLD = 30.0

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

# phrase-to-phrase conditonal probabilities
for span1,phrase1 in phrases.iteritems():
	for span2,phrase2 in phrases.iteritems():
		if overlap(span1,span2): continue
		if span1[1] <= span2[0]:
			dist = span2[0] - span1[1] + 1
			for k in range(1,dist+1):
				dir1 = phrase2phraseNeighbours[(phrase1,'neigh('+phrase2+')','<',k)] = findCondProb([phrase1],neighbours[phrase2],span1[0],span2[0],'<',k,splitCorpus)
				dir2 = phrase2phraseNeighbours[('neigh('+phrase2+')',phrase1,'>',k)] = findCondProb(neighbours[phrase2],[phrase1],span2[0],span1[0],'>',k,splitCorpus)
				threshold = 0.0
				# compare the maximum value of the two directions to the threshold
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break
		else:
			dist = span1[0] - span2[1] + 1
			for k in range(1,dist+1):
				dir1 = phrase2phraseNeighbours[(phrase1,'neigh('+phrase2+')','>',k)] = findCondProb([phrase1],neighbours[phrase2],span1[0],span2[0],'>',k,splitCorpus)
				dir2 = phrase2phraseNeighbours[('neigh('+phrase2+')',phrase1,'<',k)] = findCondProb(neighbours[phrase2],[phrase1],span2[0],span1[0],'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

for k,v in sorted(phrase2phraseNeighbours.iteritems(), key=operator.itemgetter(1)):
    sys.stderr.write('phrase2phraseNeighbours' + repr(k) + '\t' + repr(v) + '\n')

sortedPhrases = sorted(phrases.iteritems(), key=operator.itemgetter(0))
sys.stdout.write('\t' + '\t'.join(['neigh('+p[1]+')' for p in sortedPhrases]) + '\n')
for span1,phrase1 in sortedPhrases:
	sys.stdout.write(phrase1 + '\t')
	for span2,phrase2 in sortedPhrases:
		if overlap(span1,span2): sys.stdout.write('--')
		else:
			direction = '<'
			dist = 0
			if span1[1] <= span2[0]:
				dist = span2[0] - span1[1] + 1
			elif span1[0] >= span2[1]:
				direction = '>'
				dist = span1[0] - span2[1] + 1
			params = (phrase1,'neigh('+phrase2+')',direction,dist)
			if params in phrase2phraseNeighbours:
				sys.stdout.write(repr(phrase2phraseNeighbours[params][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
