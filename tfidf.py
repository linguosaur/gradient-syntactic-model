import math, sys, operator


inputFile = open(sys.argv[1])
tf = {}
df = {}
tfidf = {}
totalDocs = 0
totalWords = 0

for line in inputFile:
	splitLine = line.lower().split()
	totalDocs += 1

	for w in splitLine:
		totalWords += 1
		if w not in tf: 
			tf[w] = 1
		else: 
			tf[w] += 1

	splitLineSet = set(splitLine)
	for w in splitLineSet:
		if w not in df:
			df[w] = 1
		else:
			df[w] += 1


for w in tf:
	tfidf[w] = 1.0 * tf[w] / totalDocs * math.log(1.0 * totalDocs / df[w])

for k, v in sorted(tfidf.iteritems(), key=operator.itemgetter(1), reverse=True):
	print k + '\t' + repr(v)
print
print 'total docs:', repr(totalDocs)
print 'total words:', repr(totalWords)
