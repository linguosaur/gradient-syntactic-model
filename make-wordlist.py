import re, sys, operator


inputFile = open(sys.argv[1])
vocab = set([])

for line in inputFile:
	splitLine = line.lower().split()
	for w in splitLine:
		vocab.add(w)

for k in sorted(vocab, key=operator.itemgetter(0)):
	print k
print
print 'total words:', repr(len(vocab))
