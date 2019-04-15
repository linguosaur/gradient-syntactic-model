import sys

def addToHashedSets(item, heading, dic):
	if heading not in dic:
		dic[heading] = set([item])
	else:
		dic[heading].add(item)

	return dic

sys.stderr.write('reading in sequences file . . . ')

seqsfile = open(sys.argv[1])
seqsfileLines = seqsfile.readlines()
seqsfile.close()

sys.stderr.write('done. \n')
sys.stderr.write('number of seqs: ' + repr(len(seqsfileLines)) + '\n')

profiles = {}
BLANK = '___'

sys.stderr.write('gathering word profiles . . . \n')

for i in range(len(seqsfileLines)):
	if i % 10 == 0:
		sys.stderr.write(repr(i) + ', ')
	splitSeqFreq = seqsfileLines[i].strip().split('\t')
	seq = splitSeqFreq[0]
	freq = splitSeqFreq[1]
	splitSeq = seq.split()
	for j in range(len(splitSeq)):
		heading = splitSeq[j]
		splitSeq[j] = BLANK
		entry = ' '.join(splitSeq)
		profiles = addToHashedSets(entry, heading, profiles)
		splitSeq[j] = heading

sys.stderr.write('done.\n')
sys.stderr.write('printing . . . ')

for word in profiles:
	sys.stdout.write(word + ':\n')
	entrySet = profiles[word]
	for entry in entrySet:
		sys.stdout.write(entry + '\n')
	sys.stdout.write('\n')

sys.stderr.write('done.\n')
