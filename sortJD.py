import sys

sys.stderr.write('reading in Jaccard distance file . . . ')
jdFile = open(sys.argv[1])
jdFileLines = jdFile.readlines()
jdFile.close()
sys.stderr.write('done.\n\n')

jd = []

sys.stderr.write('reading in Jaccard distances . . . ')
i = 0
for line in jdFileLines:
	if i % 1000000 == 0:
		sys.stderr.write(repr(i/1000000) + ', ')
		sys.stderr.flush()
	i += 1
	splitLine = line.strip().split('\t')
	if len(splitLine) == 3:
		[word1, word2, distStr] = splitLine
	jd.append((float(distStr), word1, word2))
sys.stderr.write('done.\n\n')
	
jd.sort()
sys.stderr.write('printing to file . . . ')
for item in jd:
	(dist, word1, word2) = item
	sys.stdout.write('\t'.join([word1, word2, repr(dist)]) + '\n')
sys.stderr.write('done.\n\n')
