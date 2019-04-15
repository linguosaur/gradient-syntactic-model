import operator, sys

# returns P(word1|word2,dir,adj)
# dir is '<' if word1 left of word2, '>' if word1 right of word2
# corpus contains lists of sentences which are lists of words
#
# 20161012: bug 1: adjacents word1word2Freq's aren't the same when swapped *FIXED*
# 20161014: bug 2: non-adj's have probs > 1.0 (design flaw)
def findCondProb(word1,word2,pos1,pos2,direction,wordDist,corpus):
	[word1Freq,word2Freq,totalWords,word1word2Freq,word1Index,word2Index] = [0,0,0,0,0,0]
	sentNum = 0

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		word1Freq += sentence.count(word1)
		word2Freq += sentence.count(word2)
		totalWords += len(sentence)

		while sentence[startIndex:].count(word2) > 0:
			word2Index = startIndex + sentence[startIndex:].index(word2)
			if direction == '>':
				word1Index = word2Index + wordDist
				if word1Index < len(sentence):
					if sentence[word1Index] == word1:
						word1word2Freq += 1
			elif direction == '<':
				word1Index = word2Index - wordDist
				if word1Index >= 0:
					if sentence[word1Index] == word1:
						word1word2Freq += 1
			startIndex = word2Index + 1

	return (pos1,pos2,word1Freq,word2Freq,word1word2Freq,1.0*word1word2Freq/word2Freq,1.0*word1Freq/totalWords,1.0*word1word2Freq*totalWords/(word1Freq*word2Freq))


corpusFN = sys.argv[1]

splitCorpus = []
word2word = {}
sentence = 'not all those who wrote oppose the changes'
splitSentence = sentence.split()

with open(corpusFN) as corpusFile:
	for line in corpusFile:
		splitLine = line.lower().split()
		splitCorpus.append(splitLine)

# word-to-word conditonal probabilities
splitSentence = sentence.split()
for i in range(0,len(splitSentence)):
	word1 = splitSentence[i]
	for j in range(i+1,len(splitSentence)):
		word2 = splitSentence[j]
		if i < j:
			wordDist = j - i
			for k in range(1,wordDist+1):
				dir1 = word2word[(word1,word2,'<',k)] = findCondProb(word1,word2,i,j,'<',k,splitCorpus)
				dir2 = word2word[(word2,word1,'>',k)] = findCondProb(word2,word1,j,i,'>',k,splitCorpus)
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
				dir1 = word2word[(word6,word2,'>',k)] = findCondProb(word6,word2,i,j,'>',k,splitCorpus)
				dir2 = word2word[(word2,word6,'<',k)] = findCondProb(word2,word6,j,i,'<',k,splitCorpus)
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

sys.stdout.write('\t' + '\t'.join(splitSentence) + '\n')
for i in range(0,len(splitSentence)):
	sys.stdout.write(splitSentence[i] + '\t')
	for j in range(0,len(splitSentence)):
		if i == j: sys.stdout.write('--')
		else:
			wordi = splitSentence[i]
			wordj = splitSentence[j]
			direction = '<'
			if i > j:
				direction = '>'
			if (wordi,wordj,direction,abs(i-j)) in word2word:
				sys.stdout.write(repr(word2word[(wordi,wordj,direction,abs(i-j))][7]))
		sys.stdout.write('\t')
	sys.stdout.write('\n')
