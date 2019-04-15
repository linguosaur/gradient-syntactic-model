import re, sys

def readSeqs(seqsFilename):
	seqsfile = open(seqsFilename)
	seqsfileLines = seqsfile.readlines()
	seqsfile.close()
	
	seqs = {}
	for line in seqsfileLines:
		splitLine = line.strip().split('\t')
		seq = splitLine[0].strip()
		freq = splitLine[1]
		seqs[seq] = freq

	return seqs

def compareSeqLists(seqs1, seqs2, blanked1, blanked2, repl1, repl2):
	commonList = [[], []]
	
	shorterList = seqs1
	shortBlanked = blanked1
	shortRepl = repl1
	longerList = seqs2
	longBlanked = blanked2
	longRepl = repl2
	if len(seqs2) < len(seqs1):
		shorterList = seqs2
		shortBlanked = blanked2
		shortRepl = repl2
		longerList = seqs1
		longBlanked = blanked1
		longRepl = repl1

	for shortListSeq in shorterList:
		if re.search(shortBlanked, shortListSeq) != None:
			longListSeq = longRepl.join(re.split(shortBlanked, shortListSeq))
			if longListSeq in longerList:
				commonList[0].append((shortListSeq, shorterList[shortListSeq]))
				commonList[1].append((longListSeq, longerList[longListSeq]))
	return commonList

seqs1 = readSeqs(sys.argv[1])
seqs2 = readSeqs(sys.argv[2])
blanked1 = r' agency$'
blanked2 = r' corporation$'
repl1 = ' agency'
repl2 = ' corporation'
commonSeqsLists = compareSeqLists(seqs1, seqs2, blanked1, blanked2, repl1, repl2)

for seqList in commonSeqsLists:
	for seq in seqList:
		sys.stdout.write(seq[0] + '\t' + seq[1] + '\n')
	sys.stdout.write('\n')
