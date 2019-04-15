import math, operator, sys


seqFreqFile = open(sys.argv[1])
seqFreqLines = seqFreqFile.readlines()
seqFreqFile.close()
wordFreqFile = open(sys.argv[2])
wordFreqLines = wordFreqFile.readlines()
wordFreqFile.close()

wordFreqs = {}
totalFreqs = 0
for line in wordFreqLines:
	splitLine = line.strip().split('\t')
	if len(splitLine) == 2:
		[word, wordFreq] = splitLine
		wordFreqs[word] = int(wordFreq)
	elif line.startswith('total words: '):
		newSplitLine = line.strip().split(': ')
		totalFreqs = int(newSplitLine[1])

seqStrengths = {}
seqFreqs = {}
for line in seqFreqLines:
	[seq, seqFreq] = line.strip().split('\t')
	seqFreq = int(seqFreq)
	seqFreqs[seq] = seqFreq
	splitSeq = seq.split()
	baseline = totalFreqs - len(splitSeq) + 1
	for word in splitSeq:
		baseline *= 1.0 * wordFreqs[word] / totalFreqs
	if baseline > 0.0:
		seqStrengths[seq] = math.log(1.0 * seqFreq / baseline, 2)
	else:
		seqStrengths[seq] = 'NaN'

for k, v in sorted(seqStrengths.items(), key=operator.itemgetter(1), reverse=True):
	if type(v) is float:
		sys.stdout.write(k + '\t' + repr(seqFreqs[k]) + '\t' + repr(v) + '\n')
	elif type(v) is str:
		sys.stdout.write(k + '\t' + repr(seqFreqs[k]) + '\t' + v + '\n')
