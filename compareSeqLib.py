import sys
import findsimilarwordslib

__MAXDIST__ = 1000000
__jaccardDistances__ = {} # cache


def getJaccard(word1, word2, profiles):
	if word1 + '_' + word2 in __jaccardDistances__: 
		return __jaccardDistances__[word1 + '_' + word2]
	else:
		jaccard = findsimilarwordslib.jaccardDistance(profiles[word1], profiles[word2])
		__jaccardDistances__[word1 + '_' + word2] = jaccard
		__jaccardDistances__[word2 + '_' + word1] = jaccard

	return jaccard

def getJaccardWeighted(word1, word2, freqs, profiles):
	if word1 + '_' + word2 in __jaccardDistances__: 
		return __jaccardDistances__[word1 + '_' + word2]
	else:
		jaccard = findsimilarwordslib.jaccardDistanceWeighted(profiles[word1], profiles[word2], freqs)
		__jaccardDistances__[word1 + '_' + word2] = jaccard
		__jaccardDistances__[word2 + '_' + word1] = jaccard

	return jaccard

# sequences are encoded as tuples of integers
def compareSeqInside(seq1, seq2, profiles):
	if len(seq1) != len(seq2):
		sys.stderr.write('Sequences not the same length.\n')
		return

	distSum = 0.0
	for i in range(len(seq1)):
		word1 = seq1[i]
		word2 = seq2[i]
		jaccard = getJaccard(word1, word2, profiles)
		denom = 1.0 - jaccard
		if denom > 0.0:
			distSum += 1.0/denom
		else:
			distSum += __MAXDIST__

	return distSum

# sequences are encoded as tuples of integers
def compareSeqInsideWeighted(seq1, seq2, freqs, profiles):
	if len(seq1) != len(seq2):
		sys.stderr.write('Sequences not the same length.\n')
		return

	distSum = 0.0
	for i in range(len(seq1)):
		word1 = seq1[i]
		word2 = seq2[i]
		jaccard = getJaccard(word1, word2, freqs, profiles)
		denom = 1.0 - jaccard
		if denom > 0.0:
			distSum += 1.0/denom
		else:
			distSum += __MAXDIST__

	return distSum

# make sure words in sequences are in the same form as in jd
def compareSeqInsidePrepped(seq1, seq2, jd):
	if len(seq1) != len(seq2):
		sys.stderr.write('Sequences not the same length.\n')
		return

	distSum = 0.0
	for i in range(len(seq1)):
		word1 = seq1[i]
		word2 = seq2[i]
		denom = 1.0 - jd[word1][word2]
		if denom > 0.0:
			distSum += 1.0/denom
		else:
			distSum += __MAXDIST__

	return distSum
