import sys, groupSeqLib


# for a given word, get the closest n neighbours to it
def getTopN(word, jd, n):
	if word in jd:
		wordToDist = jd[word]
		sortedDists = sorted(wordToDist.keys(), key=wordToDist.__getitem__)
		return set(sortedDists[:n])

	return None

# uses external cache, *clusters*
def getClusterWithCache(word, jd, n, cache):
    if word in cache:
        return cache[word]

    cluster = getTopN(word, jd, n)
    if cluster != None:
        cache[word] = cluster
        return cluster

    return None

# read Jaccard distances (with no reflexives)
def getJD(jdFilename):
	jd = {}
	with open(jdFilename) as jdFile:
		for line in jdFile:
			[word1, word2, dist] = line.strip().split('\t')
			groupSeqLib.insert2D(word1, word2, dist, jd)
	jdFile.close()

	return jd
	
if __name__ == '__main__':
	jdFilename = sys.argv[1]
	n = 5
	
	while True:
		sys.stdout.write('word: ')
		word1 = sys.stdin.readline().strip()
	
		topN = getTopN(word1, jd, n)
		for word2 in topN:
			sys.stdout.write(word2 + '\n')
	
		sys.stdout.write('\n')
