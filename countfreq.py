import re, sys, operator


inputFile = open(sys.argv[1])
freq = {}
totalWords = 0
totalOps = 0

for line in inputFile:
	splitLine = line.lower().split()
	for w in splitLine:
		if w not in freq: freq[w] = 1
		else: freq[w] += 1
		totalWords += 1

for k, v in sorted(freq.iteritems(), key=operator.itemgetter(1), reverse=True):
	#totalOps += v * (totalWords - v)
	print k + '\t' + repr(v)
print
print 'total words:', repr(totalWords)
#print 'total comparisons:', repr(totalOps)
#print 'average frequency:', repr(1.0*totalWords/len(freq))
