import operator, sys

# 20161025: fix distance calculation in findCondProb(); make use of dist() *FIXED*

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

[parseFN,corpusFN] = sys.argv[1:3]

splitCorpus = []
phrase2phrase = {}
phrases = {}

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

# phrase-to-phrase conditonal probabilities
for span1,phrase1 in phrases.iteritems():
	for span2,phrase2 in phrases.iteritems():
		if overlap(span1,span2): continue
		if span1[1] <= span2[0]:
			dist = span2[0] - span1[1] + 1
			for k in range(1,dist+1):
				dir1 = phrase2phrase[(phrase1,phrase2,'<',k)] = findCondProb(phrase1.split(),phrase2.split(),span1[0],span2[0],'<',k,splitCorpus)
				dir2 = phrase2phrase[(phrase2,phrase1,'>',k)] = findCondProb(phrase2.split(),phrase1.split(),span2[0],span1[0],'>',k,splitCorpus)
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
				dir1 = phrase2phrase[(phrase1,phrase2,'>',k)] = findCondProb(phrase1.split(),phrase2.split(),span1[0],span2[0],'>',k,splitCorpus)
				dir2 = phrase2phrase[(phrase2,phrase1,'<',k)] = findCondProb(phrase2.split(),phrase1.split(),span2[0],span1[0],'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

for k,v in sorted(phrase2phrase.iteritems(), key=operator.itemgetter(1)):
    sys.stderr.write('phrase2phrase' + repr(k) + '\t' + repr(v) + '\n')

sortedPhrases = sorted(phrases.iteritems(), key=operator.itemgetter(0))
sys.stdout.write('\t' + '\t'.join([p[1] for p in sortedPhrases]) + '\n')
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
			if (phrase1,phrase2,direction,dist) in phrase2phrase:
				sys.stdout.write(repr(phrase2phrase[(phrase1,phrase2,direction,dist)][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
