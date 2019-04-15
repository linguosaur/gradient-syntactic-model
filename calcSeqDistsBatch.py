import operator, sys
import compareSeqLib, groupSeqLib

def insertSeq(seq,length,dic):
	if length not in dic:
		dic[length] = []
	dic[length].append(seq)

def insertDist(seq1,seq2,dist,dic):
	if seq1 not in dic:
		dic[seq1] = {}
	dic[seq1][seq2] = dist


[parseFilename,seqFilename,jdFilename] = sys.argv[1:4]
allSeqs = []
allSeqsByLength = []
jd = {}
seqDists = {}
seqsByLen = {}

with open(parseFilename) as parseFile:
	sys.stderr.write('reading in parse file . . . ')
	for line in parseFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 3:
			seq = splitLine[1]
			if seq not in allSeqs:
				allSeqs.append(seq)
	sys.stderr.write('done.\n\n')

for headSeq in allSeqs:
	allSeqsByLength.append(len(headSeq.split()))

with open(seqFilename) as seqFile:
	sys.stderr.write('reading in sequences . . . ')
	for line in seqFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 2:
			seq = splitLine[0]
			seqLen = len(seq.split())
			if seqLen in allSeqsByLength:
				insertSeq(seq,seqLen,seqsByLen)
	sys.stderr.write('done.\n\n')

with open(jdFilename) as jdFile:
	sys.stderr.write('reading in Jaccard distances . . . ')
	for line in jdFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 3:
			word1 = splitLine[0]
			word2 = splitLine[1]
			dist = float(splitLine[2])
			groupSeqLib.insert2D(word1,word2,dist,jd)
	sys.stderr.write('done.\n\n')

sys.stderr.write('calculating and printing sequence distances . . . \n')
for headSeq in allSeqs:
	i = 0
	for seq in seqsByLen[len(headSeq.split())]:
		i += 1
		if i % 10 == 0:
			sys.stderr.write(repr(i) + ', ')
			sys.stderr.flush()
		seqDist = compareSeqLib.compareSeqInsidePrepped(headSeq.split(),seq.split(),jd)
		seqDists[seq] = seqDist
	sys.stderr.write('done.\n\n')

	sys.stdout.write(headSeq + ':\n')
	for seq,dist in sorted(seqDists.items(),key=operator.itemgetter(1)):
		sys.stdout.write('\t'.join([seq,repr(dist)]) + '\n')

	seqDists = {}
	sys.stdout.write('\n')
