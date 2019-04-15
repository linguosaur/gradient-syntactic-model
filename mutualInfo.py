import sys

def addToDic(dist, dic):
	if dist not in dic:
		dic[dist] = 1
	else:
		dic[dist] += 1

	return dic

def addToPairFreqDic(word1, word2, dic):
	if word1 not in dic:
		dic[word1] = {}
	if word2 not in dic[word1]:
		dic[word1][word2] = 1
	else:
		dic[word1][word2] += 1
		
	return dic

def sumMarginals(pair, margX, margY):
	for dist in pair:
		margX[dist] = {}
		margY[dist] = {}
		for word_i in pair[dist]:
			margX[dist][word_i] = 0
			for word_j in pair[dist][word_i]:
				margX[dist][word_i] += pair[dist][word_i][word_j]

		for word_i in pair[dist]:
			for word_j in pair[dist][word_i]:
				if word_j not in margY[dist]
					margY[dist][word_j] = pair[dist][word_i][word_j]
				else:
					margY[dist][word_j] += pair[dist][word_i][word_j]

	return 

def mutualInformation(word1, word2, pair, margX, margY, totalFreq, totalSingleFreq, totalPairFreq):
	if word1 not in pair or word2 not in pair[word1]:
		return None

	p_xy = 1.0 * pair[word1][word2] / totalPairFreq
	p_xNoty = 1.0 * (margX[word1] - pair[word1][word2]) / totalPairFreq
	p_yNotx = 1.0 * (margY[word2] - pair[word1][word2]) / totalPairFreq
	p_NotxNoty = 1.0 * (totalPairFreq - pair[word1][word2]) / totalPairFreq
	p_x = 1.0 * totalSingleFreq[word1] / totalFreq
	p_Notx = 1.0 * (totalFreq - totalSingleFreq[word1]) / totalFreq
	p_y = 1.0 * totalSingleFreq[word2] / totalFreq
	p_Noty = 1.0 * (totalFreq - totalSingleFreq[word2]) / totalFreq

	mi = p_xy * math.log(p_xy / (p_x * p_y))
	mi += p_xNoty * math.log(p_xNoty / (p_x * p_Noty))
	mi += p_yNotx * math.log(p_yNotx / (p_Notx * p_y))
	mi += p_NotxNoty * math.log(p_NotxNoty / (p_Notx * p_Noty))

	return mi


margXFreqs = {}
margYFreqs = {}
pairFreqs = {}
totalFreq = 0
totalSingleFreq = {}
totalPairFreq = {}
MI = {}

textFilename = sys.argv[1]

while open(textFilename) as textFile:
	text = textFile.readlines()
textFile.close()

for line in text:
	splitline = line.lower().split()
	totalFreq += len(splitline)
	for i in range(len(splitline)):
		word_i = splitline[i]
		addToDic(word_i, totalSingleFreq)
		for j in range(i+1, len(splitline):
			word_j = splitline[j]
			dist = j-i
			addToDic(dist, totalPairFreq)
			if dist not in pairFreqs:
				pairFreqs[dist] = {}
			addToPairFreqDic(word_i, word_j, pairFreqs[dist])

sumMarginals(pairFreqs, margXFreqs, margYFreqs)

for dist in pairFreqs:
	MI[dist] = {}
	for word_i in pairFreqs[dist]:
		MI[dist][word_i] = {}
		for word_j in pairFreqs[dist][word_i]:
			MI[dist][word_i][word_j] = mutualInformation(word_i, word_j, pairFreqs[dist], margXFreqs[dist], margYFreqs[dist], totalFreq, totalPairFreq[dist])
