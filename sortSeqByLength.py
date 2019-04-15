import sys

seqFile = open(sys.argv[1])
seqFileLines = seqFile.readlines()
seqFile.close()

seqFreqs = {}
maxSeqLen = 0

sys.stderr.write('reading in sequences and frequencies . . . ')
for line in seqFileLines:
    splitLine = line.strip().split('\t')
    if (len(splitLine)) == 2:
		seq = splitLine[0]
		freq = splitLine[1]
		maxSeqLen = max(maxSeqLen, len(seq))
        seqFreqs[seq] = freq
sys.stderr.write('done.\n\n')

seqByLen = [set() for i in range(maxSeqLen)]
for seq in seqFreqs.keys():
	seqLen = len(seq.split())
	seqByLen[seqLen].add(seq)

for length in range(maxSeqLen):
	for seq in seqByLen[length]:
		sys.stdout.write(seq + '\t' + seqFreqs[seq] + '\n')
	if len(seqByLen[length]) > 0 and length < maxSeqLen - 1:
		sys.stdout.write('\n')
