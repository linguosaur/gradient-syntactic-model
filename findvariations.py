import operator, re, sys

cache = {}

# query is a string containing a regular expression
def findMatches(query):
	matches = []
	if query in cache:
		matches = cache[query]
	else:
		matches = [re.compile(query).match(seq) for seq in seqs]
		matches = [match.group(0) for match in matches if match is not None]
		cache[query] = matches

	return matches

# seq is a string
def findSubs(seq):
	splitSeq = seq.split()
	wildcard = '[\w\d$%]\S*'

	# find all the substitutions
	subs = []
	for i in range(len(splitSeq)):
		query = ' '.join(splitSeq)
		query = re.escape(query)
		query = query.split()
		query[i] = wildcard
		queryStr = '^' + ' '.join(query) + '$'
		#sys.stderr.write(queryStr + '\n')
		subs += [findMatches(queryStr)]
	
	return subs

def findIns(seq):
	splitSeq = seq.split()
	wildcard = '[\w\d$%]\S*'

	# find all the insertions
	insertions = []
	for i in range(len(splitSeq)+1):
		query = ' '.join(splitSeq)
		query = re.escape(query)
		query = query.split()
		query.insert(i, wildcard)
		queryStr = '^' + ' '.join(query) + '$'
		#sys.stderr.write(queryStr + '\n')
		insertions += [findMatches(queryStr)]

	return insertions

sys.stderr.write('reading seqsfile . . . ')

seqsfile = open(sys.argv[1])
seqsfileLines = seqsfile.readlines()
seqsfile.close()

sys.stderr.write('done.\n')
sys.stderr.write('reading sequences . . . ')

seqs = {}
for line in seqsfileLines:
	splitLine = line.strip().split('\t')
	seq = splitLine[0]
	if re.search('(^|\s)[^\w\d$%]', seq) is not None:
		continue
	freq = splitLine[1]
	seqs[seq] = int(freq)

sys.stderr.write('done.\n')
sys.stderr.write('sorting sequences . . . ')

sortedSeqs = sorted(seqs.items(), key=operator.itemgetter(1), reverse=True)

sys.stderr.write('done.\n')
sys.stderr.write('finding variants . . . \n')

for i in range(len(sortedSeqs)):
	if i % 10 == 0:
		sys.stderr.write(repr(i) + ', ')
	[seq, freq] = sortedSeqs[i]
	sys.stdout.write(seq + '\t' + repr(freq) + '\n')

	subslist = findSubs(seq)
#	insertionslist = findIns(seq)

	sys.stdout.write('subs:\n')
	for subs in subslist:
		for sub in subs: 
			sys.stdout.write(sub + '\t' + repr(seqs[sub]) + '\n')

#	sys.stdout.write('\ninsertions:\n')
#	for insertions in insertionslist:
#		sortedInsertions = sorted(insertions, key=seqs.get, reverse=True)
#		for ins in sortedInsertions:
#			sys.stdout.write(ins + '\t' + repr(seqs[ins]) + '\n')

	sys.stdout.write('\n')

sys.stderr.write('done.\n')
