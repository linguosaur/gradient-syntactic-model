import sys

seqsfile = open(sys.argv[1])
seqsfileLines = seqsfile.readlines()
seqsfile.close()

freqs = {}
for line in seqsfileLines:
	splitLine = line.strip().split('\t')
	if len(splitLine) >= 2:
		freqs[splitLine[0]] = int(splitLine[1])

sys.stderr.write('len(freqs): ' + repr(len(freqs)) + '\n')

sys.stderr.write('deleting substring sequences . . . \n')
i = 0
for seq in freqs.keys():
	i += 1
	if i % 100 == 0:
		sys.stderr.write(repr(i) + ', ')
	superseq = ''
	for superseqi in freqs:
		if seq in superseqi and seq != superseqi and freqs[seq] == freqs[superseqi]:
			superseq = superseqi
			break
	if len(superseq) > 0:
		# sys.stderr.write(seq + '\t' + repr(freqs[seq]) + '\n')
		del freqs[seq]
sys.stderr.write('\n')

sys.stderr.write('len(freqs): ' + repr(len(freqs)) + '\n')

for seq in freqs:
	sys.stdout.write(seq + '\t' + repr(freqs[seq]) + '\n')
