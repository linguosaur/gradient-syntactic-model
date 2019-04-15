import sys, getNeighboursLib


textFilename = sys.argv[1]
condProbsFilename = sys.argv[2]
jdFilename = sys.argv[3]

textLines = []
condProbs = {}
jd = {}
clusters = {}

sys.stderr.write('reading in text file . . . ')
with open(textFilename) as textFile:
	for line in textFile:
		textLines.append(line.lower().strip().split())
textFile.close()
sys.stderr.write('done.\n')

sys.stderr.write('reading in conditional probabilities file . . . ')
with open(condProbsFilename) as condProbsFile:
	for line in condProbsFile:
		splitline = line.lower().strip().split('\t')
		prediction = tuple(splitline[0][1:-1].split(', '))
		prob = float(splitline[1])
		condProbs[prediction] = prob
condProbsFile.close()
sys.stderr.write('done.\n')

sys.stderr.write('reading in Jaccard distances file . . . ')
jd = getNeighboursLib.getJD(jdFilename)
sys.stderr.write('done.\n')

for line in textLines:
