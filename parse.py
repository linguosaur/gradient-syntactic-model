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

sys.stderr.write('reading text file . . . ')
textfile = open(sys.argv[2])
textfileLines = textfile.readlines()
textfile.close()
sys.stderr.write('done.\n')

sys.stderr.write('parsing . . . \n')
sys.stderr.write('number of lines parsed:\n')
lineNum = 0
for line in textfileLines:
	lineNum += 1
	line = line.strip()
	sys.stdout.write(line + '\n')
	splitLine = line.lower().split(' ')
	for i in range(len(splitLine)-1):
		length = 2
		while i + length <= len(splitLine):
			seq = ' '.join(splitLine[i:i+length])
			if seq in seqFreqs:
				sys.stdout.write('[' + repr(i) + ',' + repr(i+length) + ']\t')
				sys.stdout.write(seq)
				sys.stdout.write('\t' + repr(seqFreqs[seq]))
				if len(seqStrengths) > 0:
					sys.stdout.write('\t' + repr(seqStrengths[seq]))
				sys.stdout.write('\n')
				length += 1
			else: break
	
	if lineNum % 10 == 0:
		sys.stderr.write(repr(lineNum) + ', ')

sys.stderr.write('\n')
