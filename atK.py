import sys

neighboursFN = sys.argv[1]

hits = 0
k = 0

with open(neighboursFN) as neighboursFile:
	headPOS = set([])
	for line in neighboursFile:
		splitLine = line.strip().split('\t')
		if len(splitLine) > 1:
			if splitLine[0][-1] == ':':
				headPOS = set(splitLine[-1].split('|'))
				k = 0
				hits = 0
			else:
				pos = set(splitLine[-1].split('|'))
				k += 1
				if len(pos & headPOS) > 0:
					hits += 1			
				prec = 1.0 * hits / k
				splitLine.append(repr(prec))
		sys.stdout.write('\t'.join(splitLine) + '\n')
