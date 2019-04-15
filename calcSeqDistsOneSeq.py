import operator, sys
import compareSeqLib, groupSeqLib

refSeq = sys.argv[3]
splitRefSeq = refSeq.split()
jd = {}
seqDists = {}

# sequence length is exactly equal to the index it's in
seqsOfSameLen = [] 

with open(sys.argv[1]) as seqFile:
	sys.stderr.write('reading in sequences . . . ')
	for line in seqFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 2:
			seq = splitLine[0]
			if len(seq.split()) == len(splitRefSeq):
				seqsOfSameLen.append(seq)
	sys.stderr.write('done.\n\n')
seqFile.close()

with open(sys.argv[2]) as jdFile:
	sys.stderr.write('reading in Jaccard distances . . . ')
	for line in jdFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 3:
			word1 = splitLine[0]
			word2 = splitLine[1]
			dist = float(splitLine[2])
			groupSeqLib.insert2D(word1, word2, dist, jd)
	sys.stderr.write('done.\n\n')
jdFile.close()

sys.stderr.write('calculating and printing sequence distances . . . \n')
i = 0
for seq in seqsOfSameLen:
	i += 1
	if i % 10 == 0:
		sys.stderr.write(repr(i) + ', ')
		sys.stderr.flush()
	seqDist = compareSeqLib.compareSeqInsidePrepped(splitRefSeq,seq.split(),jd)
	seqDists[(refSeq,seq)] = seqDist
sys.stderr.write('done.\n\n')

for seqs,dist in sorted(seqDists.items(),key=operator.itemgetter(1)):
	sys.stdout.write('\t'.join([seqs[0],seqs[1],repr(dist)]) + '\n')
