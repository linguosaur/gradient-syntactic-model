import gc, sys
import findsimilarwordslib, compareSeqLib, groupSeqLib

# sequences are sorted by length, with one blank line between sequences of different lengths
sys.stderr.write('reading sequences file . . . ')
seqFile = open(sys.argv[1])
seqFileLines = seqFile.readlines()
seqFile.close()
sys.stderr.write('done.\n\n')

sys.stderr.write('reading dictionary file . . . ')
dicFile = open(sys.argv[2])
dicFileLines = dicFile.readlines()
dicFile.close()
sys.stderr.write('done.\n\n')

sys.stderr.write('reading Jaccard distances file . . . ')
jdFile = open(sys.argv[3])
jdFileLines = jdFile.readlines()
jdFile.close()
sys.stderr.write('done.\n\n')

vocabNum = 0
dic = {}
reverseDic = {}
seqs = set() 
jd = {}
seqDist = {}
maxSeqLen = 0

sys.stderr.write('building dictionaries . . . ')
for line in dicFileLines:
	[index, word] = line.strip().split('\t')
	dic[word] = int(index)
	reverseDic[int(index)] = word
sys.stderr.write('done.\n\n')

sys.stderr.write('reading in and converting sequences . . . ')
for line in seqFileLines:
	splitLine = line.strip().split('\t')
	if (len(splitLine)) == 2:
		seq = splitLine[0]
		encodedSeq = groupSeqLib.encodeSeq(seq, dic)
        seqs.add(encodedSeq)
        maxSeqLen = max(maxSeqLen, len(encodedSeq))
sys.stderr.write('done.\n\n')

# sequence length is exactly equal to the index it's in
seqsByLen = [set() for i in range(maxSeqLen+1)]

sys.stderr.write('sorting sequences by length . . . ')
for seq in seqs:
    seqsByLen[len(seq)].add(seq)
sys.stderr.write('done.\n\n')

sys.stderr.write('reading in Jaccard distances . . . ')
for line in jdFileLines:
    splitLine = line.strip().split('\t')
    if (len(splitLine)) == 3:
		word1 = int(splitLine[0])
		word2 = int(splitLine[1])
		dist = float(splitLine[2])
		groupSeqLib.insert2D(word1, word2, dist, jd)
sys.stderr.write('done.\n\n')

outFilenameHead = '/cshome/simonmin/output/conll08st-seqdists-sorted-'
outFilenameTail = '.txt'

i = 0
for seqLen in range(len(seqsByLen)):
	sys.stderr.write('sequence length: ' + repr(seqLen) + '\n')
	
	if len(seqsByLen[seqLen]) == 0:
		continue

	sys.stderr.write('calculating sequence distances . . . \n')

	seqsThisLen = seqsByLen[seqLen]
	distsThisLen = []

	while len(seqsThisLen) > 0:
		if i % 10 == 0:
			sys.stderr.write(repr(i) + ', ')
			sys.stderr.flush()
		i += 1
		seq = seqsThisLen.pop()
		for seq2 in seqsThisLen: 
			seqDist = compareSeqLib.compareSeqInsidePrepped(seq, seq2, jd)
			distsThisLen.append((seqDist, seq, seq2))

	sys.stderr.write('done.\n\n')
	sys.stderr.write('printing sorted decoded sequence distances . . . \n')

	distsThisLen.sort()

	outFilename = outFilenameHead + repr(seqLen) + outFilenameTail
	outFile = open(outFilename, 'w')
	for item in distsThisLen:
		seq1 = groupSeqLib.decodeSeq(item[1], reverseDic)
		seq2 = groupSeqLib.decodeSeq(item[2], reverseDic)
		outFile.write(seq1 + '\t' + seq2 + '\t' + repr(item[0]) + '\n')
	outFile.close()

	gc.collect()

sys.stderr.write('done.\n\n')
