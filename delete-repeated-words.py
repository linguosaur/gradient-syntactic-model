import sys

sentFileName = sys.argv[1]

seen = []
with open(sentFileName) as sentFile:
	for line in sentFile:
		splitLine = line.strip().split()
		for word in splitLine:
			if word not in seen:
				seen.append(word)

sys.stdout.write(' '.join(seen) + '\n')
