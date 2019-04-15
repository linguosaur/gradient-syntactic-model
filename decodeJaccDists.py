import gc, sys
import findsimilarwordslib, compareSeqLib, groupSeqLib


reverseDic = {}

# read in file of indices to words
with open(sys.argv[1]) as dicFile:
	sys.stderr.write('building dictionaries . . . ')
	for line in dicFile:
		[index, word] = line.strip().split('\t')
		reverseDic[int(index)] = word
	sys.stderr.write('done.\n\n')
dicFile.close()

# read in file of indexed words to Jaccard distances
lineNum = 0
with open(sys.argv[2]) as jdFile:
	sys.stderr.write('reading in Jaccard distances . . . ')
	for line in jdFile:
		lineNum += 1
		if lineNum % 100000 == 0:
			sys.stderr.write(repr(lineNum) + ', ')
		splitLine = line.strip().split('\t')
		if (len(splitLine)) == 3:
			word1 = reverseDic[int(splitLine[0])]
			word2 = reverseDic[int(splitLine[1])]
			dist = splitLine[2]
			sys.stdout.write('\t'.join([word1, word2, dist]) + '\n')
	sys.stderr.write('done.\n\n')
jdFile.close()
