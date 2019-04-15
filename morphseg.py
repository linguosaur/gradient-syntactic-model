import difflib, re, sys, operator


# returns the longest common sequence of letters between w1 and w2
# common sequence may be discontinuous
def findBase(w1, w2):
	common = []
	w1affixes = []
	w2affixes = []
	difference = difflib.SequenceMatcher()
	difference.set_seqs(w1, w2)
	matching_blocks = difference.get_matching_blocks()
	w1pointer = 0
	w2pointer = 0
	for match_i in range(len(matching_blocks)):
		match = matching_blocks[match_i]
		print match
		subseq = w1[match[0]:match[0]+match[2]]
		if subseq != '':
			common.append(subseq)

		if match_i < len(matching_blocks)-1:
			# gather prefixes and infixes
			if match[0] > w1pointer: 
				w1affixes.append(w1[w1pointer:match[0]])
			if match[1] > w2pointer:
				w2affixes.append(w2[w2pointer:match[1]])
			w1pointer = match[0] + match[2]
			w2pointer = match[1] + match[2]
	
			# gather suffixes
			if match_i == len(matching_blocks)-2: 
				w1pointer = match[0] + match[2]
				w2pointer = match[1] + match[2]
				if w1pointer < len(w1):
					w1affixes.append(w1[w1pointer:])
				if w2pointer < len(w2):
					w2affixes.append(w2[w2pointer:])

	return [common, w1affixes, w2affixes]

wordlistFile = open(sys.argv[1])
vocab = set([])

sys.stderr.write('reading word list . . . ')
for line in wordlistFile:
	word = line.rstrip()
	vocab.add(word)
sys.stderr.write('done\n')

# search for a pair of words that share most of their letters, in the same order
# with as few interruptions as possible
# or define them
word1 = 'ohittako'
word2 = 'ohittamaan'

# find their difference
[base, affixes1, affixes2] = findBase(word1, word2)
print base
print affixes1
print affixes2

# find other words with this base
wordSet1 = set([])
for word in vocab:
	[common, affixes1, affixes2] = findBase(base, word)
	if common == base:
		wordSet1.add(word)
