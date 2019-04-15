import gc, sys
import findsimilarwordslib, compareSeqLib, groupSeqLib

def addToSeqsByLen(seq, seqsByLen):
	seqLen = len(seq)
	while len(seqsByLen) <= seqLen:
		seqsByLen.append(set())
	seqsByLen[seqLen].add(seq)

def reprEncodedSeq(seq):
	reprCodes = []
	for code in seq:
		reprCodes.append(repr(code))

	return ', '.join(reprCodes)

dic = {}
reverseDic = {}
jd = {}

# sequence length is exactly equal to the index it's in
seqsByLen = [] 

with open(sys.argv[1]) as dicFile:
	sys.stderr.write('building dictionaries . . . ')
	for line in dicFile:
		[index, word] = line.strip().split('\t')
		dic[word] = int(index)
		reverseDic[int(index)] = word
	sys.stderr.write('done.\n\n')
dicFile.close()
gc.collect()

with open(sys.argv[2]) as seqFile:
	sys.stderr.write('reading in and converting sequences . . . ')
	for line in seqFile:
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 2:
			seq = splitLine[0]
			encodedSeq = groupSeqLib.encodeSeq(seq, dic)
	        addToSeqsByLen(encodedSeq, seqsByLen)
	sys.stderr.write('done.\n\n')
seqFile.close()
gc.collect()

with open(sys.argv[3]) as jdFile:
	sys.stderr.write('reading in Jaccard distances . . . ')
	for line in jdFile:
	    splitLine = line.strip().split('\t')
	    if (len(splitLine)) == 3:
			word1 = int(splitLine[0])
			word2 = int(splitLine[1])
			dist = float(splitLine[2])
			groupSeqLib.insert2D(word1, word2, dist, jd)
	sys.stderr.write('done.\n\n')
jdFile.close()
gc.collect()

outFilenameHead = sys.argv[4]
outFilenameTail = '.txt'

sys.stderr.write('calculating and printing sequence distances . . . \n')
i = 0
for seqLen in range(len(seqsByLen)):
	if len(seqsByLen[seqLen]) == 0:
		continue

	seqsThisLen = seqsByLen[seqLen]

	sys.stderr.write('sequence length: ' + repr(seqLen) + '\n')

	outFilename = outFilenameHead + repr(seqLen) + outFilenameTail
	with open(outFilename, 'w') as outFile:
		while len(seqsThisLen) > 0:
			if i % 10 == 0:
				sys.stderr.write(repr(i) + ', ')
				sys.stderr.flush()
			i += 1
			seq1 = seqsThisLen.pop()
			for seq2 in seqsThisLen: 
				seqDist = compareSeqLib.compareSeqInsidePrepped(seq1, seq2, jd)
				outFile.write(reprEncodedSeq(seq1) + '\t' + reprEncodedSeq(seq2) + '\t' + repr(seqDist) + '\n')
	outFile.close()
	gc.collect()

sys.stderr.write('done.\n\n')
