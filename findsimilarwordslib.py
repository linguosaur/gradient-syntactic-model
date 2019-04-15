import operator, sys

def getSharedPatterns(wordlist):
	set1 = profiles[wordlist.pop()]
	intersect = set1
	while len(wordlist) > 0:
		set2 = profiles[wordlist.pop()]
		intersect = set1 & set2
		set1 = intersect
	return intersect

def jaccardDistance(set1, set2):
	jaccardDist = 1.0 - 1.0 * len(set1 & set2) / len(set1 | set2)
	return jaccardDist

# the less frequent the context, the more informative it is
def jaccardDistanceWeighted(set1, set2, freqs):
	intersection = set1 & set2
	union = set1 | set2
	intersectionSize = 0.0
	unionSize = 0.0
	totalWordTypes = len(freqs.keys())

	for item in intersection:
		intersectionSize += 1.0 - 1.0 * freqs[item] / totalWordTypes
	for item in union:
		unionSize += 1.0 - 1.0 * freqs[item] / totalWordTypes

	jaccardDistWeighted = 1.0 - 1.0 * intersectionSize / unionSize
	return jaccardDistWeighted

def addToDic(pattern, dic):
	if pattern in dic:
		dic[pattern] += 1
	else:
		dic[pattern] = 1

def addToDoubleDict(item, dblarray, key1, key2):
	if key1 not in dblarray:
		dblarray[key1] = {}
	dblarray[key1][key2] = item
	dblarray[key2][key1] = item
	return

def fillProfiles(profileTable, lines):
	heading = ''
	isReading = False
	for line in lines:
		line = line.rstrip()
		if line == '':
			isReading = False
		elif line[-1] == ':':
			heading = line[:-1]
			profileTable[heading] = set()
			isReading = True
		elif isReading:
			profileTable[heading].add(line)

def fillProfilesFreqs(profileTable, freqsTable, lines):
	heading = ''
	isReading = False
	for line in lines:
		line = line.rstrip()
		if line == '':
			isReading = False
		elif line[-1] == ':':
			heading = line[:-1]
			profileTable[heading] = set()
			isReading = True
		elif isReading:
			profileTable[heading].add(line)
			addToDic(line, freqsTable)
