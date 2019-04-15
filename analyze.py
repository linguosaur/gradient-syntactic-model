import operator, sys

# returns P(word1|word2,dir,adj)
# dir is '<' if word1 left of word2, '>' if word1 right of word2
# corpus contains lists of sentences which are lists of words
#
# 20161012: bug 1: adjacents word1word2Freq's aren't the same when swapped *FIXED*
# 20161014: bug 2: non-adj's have probs > 1.0 (design flaw)
def findCondProb(word1,word2,dir,adj,corpus):
	[word2Freq,word1word2Freq,word1Index,word2Index] = [0,0,0,0]
	sentNum = 0

	for sentence in corpus:
		sentNum += 1
		startIndex = 0
		word2Freq += sentence.count(word2)

		while sentence[startIndex:].count(word2) > 0:
			word2Index = startIndex + sentence[startIndex:].index(word2)
			if adj:
				if dir == '>':
					word1Index = word2Index + 1
					if word1Index < len(sentence):
						if sentence[word1Index] == word1:
							word1word2Freq += 1
				elif dir == '<':
					word1Index = word2Index - 1
					if word1Index >= 0:
						if sentence[word1Index] == word1:
							word1word2Freq += 1
			elif not adj:
				if dir == '>':
					word1word2Freq += sentence[word2Index+2:len(sentence)].count(word1)
				elif dir == '<':
					word1word2Freq += sentence[0:word2Index-1].count(word1)
			startIndex = word2Index + 1

	return (word1word2Freq, word2Freq, 1.0 * word1word2Freq / word2Freq)


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
			if j - i == 1:
				word2word[(word1,word2,'<',True)] = findCondProb(word1,word2,'<',True,splitCorpus)
				word2word[(word2,word1,'>',True)] = findCondProb(word2,word1,'>',True,splitCorpus)
			else:
				word2word[(word1,word2,'<',False)] = findCondProb(word1,word2,'<',False,splitCorpus)
				word2word[(word2,word1,'>',False)] = findCondProb(word2,word1,'>',False,splitCorpus)
		elif i > j:
			if i - j == 1:
				word2word[(word1,word2,'>',True)] = findCondProb(word1,word2,'>',True,splitCorpus)
				word2word[(word2,word1,'<',True)] = findCondProb(word2,word1,'<',True,splitCorpus)
			else:
				word2word[(word1,word2,'>',False)] = findCondProb(word1,word2,'>',False,splitCorpus)
				word2word[(word2,word1,'<',False)] = findCondProb(word2,word1,'<',False,splitCorpus)


for k in sorted(word2word.keys(), key=operator.itemgetter(0,1,2,3)):
	sys.stdout.write('word2word' + repr(k) + '\t' + repr(word2word[k]) + '\n')	
