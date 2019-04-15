import operator, sys
import findsimilarwordslib

def findSortedNeighbours(word, profiles):
	jaccardSimilarities = {}
	for word2 in profiles:
		if word2 != word and len(profiles[word2]) >= PROFILE_SIZE_THRESHOLD:
			jaccardSimilarities[word2] = findsimilarwordslib.jaccardDistance(profiles[word], profiles[word2])
	sortedNeighbours = sorted(jaccardSimilarities.iteritems(), key=operator.itemgetter(1))

	return sortedNeighbours

switch = sys.argv[1]

PROFILE_SIZE_THRESHOLD = 0
NUM_OF_HITS = 3
CLUSTER_SWITCH = '--cluster'
TOPN_SWITCH = '--topN'
COMPARE_SWITCH = '--compare'
RANGE_SWITCH = '--range'
ALLN_SWITCH = '--allN'
BATCH_SWITCH = '--batch'

profilesFN = sys.argv[2]
if switch == TOPN_SWITCH or switch == RANGE_SWITCH:
	profilesFN = sys.argv[3]
profilesFileLines = []

with open(profilesFN) as profilesFile:
	sys.stderr.write('reading profiles file . . . ')
	profilesFileLines = profilesFile.readlines()
	sys.stderr.write('done.\n\n')

profiles = {}
findsimilarwordslib.fillProfiles(profiles, profilesFileLines)

if switch == BATCH_SWITCH:
	sentence = ''
	sentFN = sys.argv[3]
	if switch == TOPN_SWITCH or switch == RANGE_SWITCH:
		sentFN = sys.argv[4]
	with open(sentFN) as sentFile:
		sentence = sentFile.readline().lower().strip()
	splitSent = sentence.split()
	for word in splitSent:
		sortedNeighbours = findSortedNeighbours(word, profiles)
		sys.stdout.write(word + ':\n')
		for neighbour in sortedNeighbours:
			sys.stdout.write(neighbour[0] + '\t' + repr(neighbour[1]) + '\n')
		sys.stdout.write('\n')
	exit()

while True:
	sys.stderr.write('word/sentence: ')
	word1 = sys.stdin.readline().strip()

	if switch == CLUSTER_SWITCH:
		clusterList = [word1]
		commonPatterns = profiles[word1]
		mostSimilarWords = []
		for i in range(NUM_OF_HITS):
			closestWord = ''
			minDist = 1.0
			for word2 in profiles:
				if word2 not in clusterList and len(profiles[word2]) >= PROFILE_SIZE_THRESHOLD:
					dist = findsimilarwordslib.jaccardDistance(commonPatterns, profiles[word2])
					if dist < minDist:
						closestWord = word2
						minDist = dist
			if closestWord != '':
				clusterList.append(closestWord)
				mostSimilarWords.append((closestWord, minDist))
				commonPatterns = commonPatterns & profiles[closestWord]

		sys.stdout.write('First ' + repr(NUM_OF_HITS) + ' words clustered with \'' + word1 + '\', and their Jaccard distances to the cluster upon joining it:\n')
		for word2 in mostSimilarWords:
			sys.stdout.write(word2[0] + '\t' + repr(word2[1]) + '\n')
		sys.stdout.write('\n')

	elif switch == TOPN_SWITCH:
		n = int(sys.argv[sys.argv.index(TOPN_SWITCH)+1])
		sortedNeighbours = findSortedNeighbours(word1, profiles)
		if n <= len(sortedNeighbours):
			sys.stdout.write(repr(n) + ' closest words to \'' + word1 + '\' by Jaccard distance:\n')
		else:
			sys.stdout.write('Only ' + len(sortedNeighbours) + ' words available:\n')
		for i in range(min(n,len(sortedNeighbours))):
			neighbour = sortedNeighbours[i]
			sys.stdout.write(neighbour[0] + '\t' + repr(neighbour[1]) + '\n')
		sys.stdout.write('\n')

	# will not use
	elif switch == RANGE_SWITCH:
		radius = float(sys.argv.index(RANGE_SWITCH)+1)
		jaccardSimilarities = {}
		for word2 in profiles:
			if word2 != word1 and len(profiles[word2]) >= PROFILE_SIZE_THRESHOLD:
				jaccardSimilarities[word2] = findsimilarwordslib.jaccardDistance(profiles[word1], profiles[word2])
		sortedNeighbours = sorted(jaccardSimilarities.iteritems(), key=operator.itemgetter(1))
		sys.stdout.write('Words within a distance of ' + repr(radius) + ' of ' + word1 + ':\n')
		for neighbour in sortedNeighbours:
			if neighbour[1] < radius:
				sys.stdout.write(neighbour[0] + '\t' + repr(neighbour[1]) + '\n')
		sys.stdout.write('\n')

	elif switch == COMPARE_SWITCH:
		sys.stdout.write('word: ')
		word2 = sys.stdin.readline().strip()
		sys.stdout.write('Jaccard distance between \'' + word1 + '\' and \'' + word2 + '\': ')
		sys.stdout.write(repr(findsimilarwordslib.jaccardDistance(profiles[word1], profiles[word2])) + '\n')
		sys.stdout.write('weighted Jaccard distance between \'' + word1 + '\' and \'' + word2 + '\': ')
		sys.stdout.write(repr(findsimilarwordslib.jaccardDistance(profiles[word1], profiles[word2])))
		sys.stdout.write('\n\n')

	elif switch == ALLN_SWITCH:
		sortedNeighbours = findSortedNeighbours(word1, profiles)
		sys.stdout.write('Closest words to \'' + word1 + '\' by Jaccard distance (all):\n')
		sys.stdout.write(word1 + '\t--\n')
		for neighbour in sortedNeighbours:
			sys.stdout.write(neighbour[0] + '\t' + repr(neighbour[1]) + '\n')
		sys.stdout.write('\n')


