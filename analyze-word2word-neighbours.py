import operator, sys

# order of words in list is from most to least similar to headword
def insertNeigh(headword, neighbour, dic):
	if headword not in dic:
		dic[headword] = []
	dic[headword].append(neighbour)

	return

def groupCount(wordset,sentence):
	count = 0
	for word in sentence:
		if word in wordset:
			count += 1

	return count

def groupIndex(wordset,sentence):
	for i in range(len(sentence)):
		if sentence[i] in wordset:
			return i

	raise ValueError

# returns P(word1|word2,dir,adj)
# dir is '<' if word1 left of word2, '>' if word1 right of word2
# corpus contains lists of sentences which are lists of words
def findCondProb(set1,set2,pos1,pos2,direction,wordDist,corpus):
	[set1Freq,set2Freq,totalWords,set1set2Freq,set1Index,set2Index] = [0,0,0,0,0,0]
	sentNum = 0

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		set1Freq += groupCount(set1,sentence)
		set2Freq += groupCount(set2,sentence)
		totalWords += len(sentence)

		while groupCount(set2,sentence[startIndex:]) > 0:
			set2Index = startIndex + groupIndex(set2,sentence[startIndex:])
			if direction == '>':
				set1Index = set2Index + wordDist
				if set1Index < len(sentence):
					if sentence[set1Index] in set1:
						set1set2Freq += 1
			elif direction == '<':
				set1Index = set2Index - wordDist
				if set1Index >= 0:
					if sentence[set1Index] in set1:
						set1set2Freq += 1
			startIndex = set2Index + 1

	return (pos1,pos2,set1Freq,set2Freq,set1set2Freq,1.0*set1set2Freq/set2Freq,1.0*set1Freq/totalWords,1.0*set1set2Freq*totalWords/(set1Freq*set2Freq))


[sentFN,neighFN,corpusFN] = sys.argv[1:4]

splitCorpus = []
neighbours = {}
word2word = {}
THRESHOLD = 0.95

sentence = ''
with open(sentFN) as sentFile:
	sentence = sentFile.readline().lower().strip()
splitSentence = sentence.split()

with open(corpusFN) as corpusFile:
	for line in corpusFile:
		splitLine = line.strip().lower().split()
		splitCorpus.append(splitLine)

with open(neighFN) as neighFile:
	headword = ''
	for line in neighFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) == 1 and splitLine[0] != '' and splitLine[0][-1] == ':': 
			headword = splitLine[0][0:-1]
			sys.stderr.write('headword: ' + headword + '\n')
			neighbours[headword] = []
		elif len(splitLine) == 2:
			[word,score] = splitLine
			if float(score) <= THRESHOLD:
				neighbours[headword].append(word)

# word-to-word conditonal probabilities
splitSentence = sentence.split()
for i in range(0,len(splitSentence)):
	word1 = splitSentence[i]
	sys.stderr.write('word1: ' + word1 + '\n')
	for j in range(i+1,len(splitSentence)):
		word2 = splitSentence[j]
		sys.stderr.write('word2: ' + word2 + '\n')
		if i < j:
			wordDist = j - i
			for k in range(1,wordDist+1):
				dir1 = word2word[('neigh('+word1+')','neigh('+word2+')','<',k)] = findCondProb(neighbours[word1],neighbours[word2],i,j,'<',k,splitCorpus)
				dir2 = word2word[('neigh('+word2+')','neigh('+word1+')','>',k)] = findCondProb(neighbours[word2],neighbours[word1],j,i,'>',k,splitCorpus)
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
				dir1 = word2word[('neigh('+word1+')','neigh('+word2+')','>',k)] = findCondProb(neighbours[word1],neighbours[word2],i,j,'>',k,splitCorpus)
				dir2 = word2word[('neigh('+word2+')','neigh('+word1+')','<',k)] = findCondProb(neighbours[word2],neighbours[word1],j,i,'<',k,splitCorpus)
				threshold = 0.0
				if dir1[5] >= dir2[5]:
					threshold = dir1[6]
					if dir1[5] < threshold: break
				else:
					threshold = dir2[6]
					if dir2[5] < threshold: break

sys.stderr.write(sentence + '\n\n')
for k in sorted(word2word.keys(), key=operator.itemgetter(0,1,2,3)):
    sys.stderr.write('word2word' + repr(k) + '\t' + repr(word2word[k]) + '\n')

sys.stdout.write('\t' + '\t'.join(['neigh('+w+')' for w in splitSentence]) + '\n')
for i in range(0,len(splitSentence)):
	sys.stdout.write('neigh('+splitSentence[i]+')' + '\t')
	for j in range(0,len(splitSentence)):
		if i == j: sys.stdout.write('--')
		else:
			wordi = splitSentence[i]
			wordj = splitSentence[j]
			direction = '<'
			if i > j:
				direction = '>'
			if ('neigh('+wordi+')','neigh('+wordj+')',direction,abs(i-j)) in word2word:
				sys.stdout.write(repr(word2word[('neigh('+wordi+')','neigh('+wordj+')',direction,abs(i-j))][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
