import operator, re, sys

sys.stderr.write('reading seqsfile . . . ')

seqsfile = open(sys.argv[1])
seqsfileLines = seqsfile.readlines()
seqsfile.close()
sys.stderr.write('done.\n')

sys.stderr.write('reading sequences . . . ')

seqFreqs = {}
seqStrengths = {}
for line in seqsfileLines:
	splitLine = line.strip().split('\t')
	seq = splitLine[0]
	freq = splitLine[1]
	seqFreqs[seq] = int(freq)
	if len(splitLine) == 3:
		seqStrength = splitLine[2]
		seqStrengths[seq] = float(seqStrength)

sys.stderr.write('done.\n')

sys.stderr.write('reading POS file . . . ')
posfile = open(sys.argv[2])
posfileLines = posfile.readlines()
posfile.close()
sys.stderr.write('done.\n')

sys.stderr.write('reading text file . . . ')
textfile = open(sys.argv[3])
textfileLines = textfile.readlines()
textfile.close()
sys.stderr.write('done.\n')

sys.stderr.write('parsing . . . \n')
sys.stderr.write('number of lines parsed:\n')
for lineNum in range(len(textfileLines)):
	if lineNum % 10 == 0:
		sys.stderr.write(repr(lineNum) + ', ')

	posline = posfileLines[lineNum].strip()
	textline = textfileLines[lineNum].strip()
	sys.stdout.write(textline + '\n')
	sys.stdout.write(posline + '\n')
	splitLine = posline.lower().split(' ')
	seqsByPosition = {}
	for i in range(len(splitLine)-1):
		length = 2
		while i + length <= len(splitLine):
			seq = ' '.join(splitLine[i:i+length])
			if seq in seqFreqs:
				if seq in seqStrengths:
					seqsByPosition[(i,i+length)] = (seqStrengths[seq], seqFreqs[seq], seq)
				else:
					seqsByPosition[(i,i+length)] = ('--', seqFreqs[seq], seq)
				length += 1
			else: break

	# sort sequences in sentence by strength, then by frequency
	for k, v in sorted(seqsByPosition.items(), key=operator.itemgetter(1), reverse=True):
		(seqStrength, seqFreq, seq) = v
		sys.stdout.write('[' + repr(k[0]) + ',' + repr(k[1]) + ']\t')
		sys.stdout.write(seq)
		sys.stdout.write('\t' + repr(seqFreq))
		sys.stdout.write('\t' + repr(seqStrength))
		sys.stdout.write('\n')

sys.stderr.write('\n')
