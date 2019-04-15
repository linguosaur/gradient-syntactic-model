import sys

[dicFN,wordsFN] = sys.argv[1:3]

word2pos = {}
with open(dicFN) as dicFile:
	for line in dicFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) < 2: continue
		word = splitLine[0]
		pos = splitLine[1]
		word2pos[word] = pos

with open(wordsFN) as wordsFile:
	for line in wordsFile:
		splitLine = line.strip().split('\t')
		word = splitLine[0]
		if word != '': 
			tags = ''
			if word[-1] == ':':
				word = word[0:-1]
			if word in word2pos:
				tags = word2pos[word]
			else:
				tags = '??'
			splitLine.append(tags)
		sys.stdout.write('\t'.join(splitLine) + '\n')
