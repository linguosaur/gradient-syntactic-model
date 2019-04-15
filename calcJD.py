import operator, sys
import findsimilarwordslib

sys.stderr.write('reading profiles file . . . ')
profilesFile = open(sys.argv[1])
profilesFileLines = profilesFile.readlines()
profilesFile.close()
sys.stderr.write('done.\n\n')

profiles = {}
patternTypeFreqs = {}
finishedWord1s = set()

findsimilarwordslib.fillProfiles(profiles, patternTypeFreqs, profilesFileLines)

w1 = 0
for word1 in profiles.keys():
	if w1 % 10 == 0:
		sys.stderr.write(repr(w1) + ', ')
	w1 += 1
	for word2 in set(profiles.keys()) - finishedWord1s:
		dist = findsimilarwordslib.jaccardDistance(profiles[word1], profiles[word2])
		sys.stdout.write(word1 + '\t' + word2 + '\t' + repr(dist) + '\n')
	finishedWord1s.add(word1)
sys.stderr.write('\n')
