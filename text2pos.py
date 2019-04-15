import sys

depFilename = sys.argv[1]

with open(depFilename) as depFile:
	sentence = []
	for line in depFile:
		splitline = line.strip().split('\t')
		if len(splitline) > 3:
			pos = splitline[3] # column 4 is gold standard POS tag
			sentence.append(pos)
		else:
			sys.stdout.write(' '.join(sentence) + '\n')
			sentence = []
depFile.close()
