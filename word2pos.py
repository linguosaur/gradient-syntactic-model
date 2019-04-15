import sys
from operator import itemgetter

depFN = sys.argv[1]
word2pos = {}

with open(depFN) as depFile:
	for line in depFile:
		splitline = line.strip().split()
		if len(splitline) < 4: continue
		word = splitline[1].lower()
		pos = splitline[3]
		if word in word2pos:
			if pos not in word2pos[word]:
				word2pos[word].append(pos)
		else:
			word2pos[word] = [pos]

for w, p in sorted(word2pos.items(), key=itemgetter(0)):
	sys.stdout.write('\t'.join([w,'|'.join(p)]) + '\n')
