import sys

# look for phrase in corpus; return POS tags in list
# phrase is a string
def getPOStags(phrase,corpus,corpusWords,wordIndices):
	posTags = []
	splitPhrase = phrase.split()
	firstWord = splitPhrase[0]
	firstWordIndices = []
	if firstWord in wordIndices:
		firstWordIndices = wordIndices[firstWord]
	else:
		firstWordIndices = [i for i in range(len(corpusWords)) if corpusWords[i] == firstWord]
		wordIndices[firstWord] = firstWordIndices # cache
	for firstWordIndex in firstWordIndices:
		for i in range(1,len(splitPhrase)):
			if corpusWords[firstWordIndex+i] != splitPhrase[i]:
				break
		else:
			tagSeq = [pair[1] for pair in corpus[firstWordIndex:firstWordIndex+len(splitPhrase)]]
			if tagSeq not in posTags:
				posTags.append(tagSeq)
	return posTags

[depFN,wordsFN] = sys.argv[1:3]

phraseLines = []
sys.stderr.write('reading in phrases ... ')
with open(wordsFN) as wordsFile:
	for line in wordsFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) < 2: 
			sys.stdout.write('\t'.join(splitLine) + '\n')
			continue
		phraseLines.append(splitLine)
sys.stderr.write('... done\n')
sys.stderr.write('len(phraseLines): ' + repr(len(phraseLines)) + '\n')

corpus = [] # 2-tuples, (word,POS), of whole corpus
sys.stderr.write('reading in corpus ... ')
with open(depFN) as depFile:
	for line in depFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) < 4:
			corpus.append(('',''))
			continue
		word = splitLine[1].lower()
		pos = splitLine[3]
		corpus.append((word,pos))
corpusWords = [pair[0] for pair in corpus]
sys.stderr.write('... done\n')
sys.stderr.write('len(corpus): ' + repr(len(corpus)) + '\n')
sys.stderr.write('len(corpusWords): ' + repr(len(corpusWords)) + '\n')

wordIndices = {} # cache: maps word to indices in corpus and corpusWords
for phraseLine in phraseLines:
	sys.stdout.write('\t'.join(phraseLine) + '\t')
	phrase = phraseLine[0]
	posTagSeqStrs = []
	posTagSeqs = getPOStags(phrase,corpus,corpusWords,wordIndices)
	for posTagSeq in posTagSeqs:
		posTagSeqStrs.append(' '.join(posTagSeq))
	sys.stdout.write(';'.join(posTagSeqStrs) + '\n')
