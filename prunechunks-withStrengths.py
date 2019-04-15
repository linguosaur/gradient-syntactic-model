import sys

# unfinished

seqsfile = open(sys.argv[1])
seqsfileLines = seqsfile.readlines()
seqsfile.close()

freqs = {}
strengths = {}
for line in seqsfileLines:
	if len(splitLine) == 3:
		[seq,freq,strength] = line.strip().split('\t')
		freqs[seq] = int(freq)
		strengths[seq] = float(strength)

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
		del freqs[seq]
sys.stderr.write('\n')

sys.stderr.write('len(freqs): ' + repr(len(freqs)) + '\n')

for seq in freqs:
	sys.stdout.write(seq + '\t' + repr(freqs[seq]) + '\n')
