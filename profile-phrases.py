import sys

def addToHashedSets(item, heading, dic):
	if heading not in dic:
		dic[heading] = set([item])
	else:
		dic[heading].add(item)

	return dic

# replaces the *subNumber-th* occurence of *sub* in *string* with *replace*
# subNumber for first occurence is 1
def countReplace(sub, replace, string, subNumber):
	index = 0
	replaced = string
	for i in range(subNumber):
		index = replaced.index(sub)
		replaced = replaced.replace(sub, replace, 1)

	return string[0:index] + replaced[index:]

sys.stderr.write('reading in sequences file . . . ')

with open(sys.argv[1]) as seqsFile:
	seqsFileLines = seqsFile.readlines()

sys.stderr.write('done. \n')
sys.stderr.write('number of seqs: ' + repr(len(seqsFileLines)) + '\n')

seqs = set([])
profiles = {}
BLANK = '___'

sys.stderr.write('gathering word profiles . . . \n')

for i in range(len(seqsFileLines)):
	splitLine = seqsFileLines[i].strip().split('\t')
	seqs.add(splitLine[0])

for seq in seqs:
	sys.stderr.write('seq: ' + seq + '\n')
	embeddedSeqs = []
	for s in seqs: 
		if s != seq and s in seq:
			splitS = s.split()
			splitSeq = seq.split()
			if splitS[0] in splitSeq:
				splitSIndex = splitSeq.index(splitS[0])
				if splitS == splitSeq[splitSIndex:splitSIndex+len(splitS)]:
					embeddedSeqs.append(s)
	sys.stderr.write('embedded seqs: ' + repr(embeddedSeqs) + '\n')
	for emSeq in embeddedSeqs:
		timesInSeq = seq.count(emSeq)
		for i in range(1,timesInSeq+1):
			context = countReplace(emSeq, BLANK, seq, i)
			sys.stderr.write('context: ' + context + '\n')
			profiles = addToHashedSets(context, emSeq, profiles)
			sys.stderr.write('number of profiles: ' + repr(len(profiles)) + '\n')

sys.stderr.write('done.\n')
sys.stderr.write('printing . . . ')

for phrase in profiles:
	sys.stdout.write(phrase + ':\n')
	entrySet = profiles[phrase]
	for entry in entrySet:
		sys.stdout.write(entry + '\n')
	sys.stdout.write('\n')

sys.stderr.write('done.\n')
