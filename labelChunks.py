# assign the same label to sequences that differ by only one word
# e.g. "in the navy" and "in the house"
# leave all other sequences unlabeled

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
		seqs[seq] = int(freq)

	return seqs

def addToTableOfSets(value, key, table):
	if key not in table:
		table[key] = set([value])
	else:
		table[key].add(value)

sys.stderr.write('reading in sequences . . . ')
seqs = readSeqs(sys.argv[1])
sys.stderr.write('done\n')

seqIDstrs = {} # maps each sequence to its set of ID strings
unclaimedPos = {} # maps each sequence to a list of positions yet to be blanked
reverseIndex = {} # maps each ID str to a set of sequences
idnum = 0

splitSeqs = []

sys.stderr.write('listing unclaimed positions . . . ')
for seq in seqs:
	splitSeq = seq.split()
	splitSeqs.append(splitSeq)
	unclaimedPos[seq] = range(len(splitSeq))
sys.stderr.write('done\n')

sys.stderr.write('finding one-offs . . . \n')
seqnum = 0
for seq in seqs:
	sys.stderr.write('seq: ' + seq + '\n')
	splitSeq = seq.split()
	indices = list(unclaimedPos[seq])
	for i in indices:
		splitOneOffs = [splitSeq2 for splitSeq2 in splitSeqs 
					if len(splitSeq2) == len(splitSeq) 
					and splitSeq2[0:i] == splitSeq[0:i] 
					and splitSeq2[i] != splitSeq[i] 
					and splitSeq2[i+1:] == splitSeq[i+1:]
					]
		if len(splitOneOffs) > 0:
			idstr = repr(idnum) + '-' + repr(i) # [seqID no.]-[position of word being varied in this sequence]
			idnum += 1
			sys.stdout.write(idstr + ':\n')
			sys.stdout.flush()
			
			addToTableOfSets(idstr, seq, seqIDstrs)
			addToTableOfSets(seq, idstr, reverseIndex)
			unclaimedPos[seq].remove(i)
			sys.stdout.write(seq + '\t' + repr(seqs[seq]) + '\n')

			for splitOneOff in splitOneOffs:
				oneOff = ' '.join(splitOneOff)
				addToTableOfSets(idstr, oneOff, seqIDstrs)
				addToTableOfSets(oneOff, idstr, reverseIndex)
				unclaimedPos[oneOff].remove(i)
				sys.stdout.write(oneOff + '\t' + repr(seqs[oneOff]) + '\n')
				sys.stdout.flush()
	seqnum += 1
	if seqnum % 10 == 0:
		sys.stderr.write(repr(seqnum) + '\n')
sys.stderr.write('done\n')
