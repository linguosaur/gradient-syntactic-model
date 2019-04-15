import math, sys

def insertTable(key, value, table):
	if key not in table:
		table[key] = []

	table[key].append(value)

def insertFreqTable(key, table):
	if key not in table:
		table[key] = 1
	else:
		table[key] += 1

def insert2DFreqTable(key1, key2, table):
	if key1 not in table:
		table[key1] = {}

	if key2 in table[key1]:
		table[key1][key2] += 1
	else:
		table[key1][key2] = 1


treeFilename = sys.argv[1]

freqs = {}
wordFreqsByPOS = {} # e.g. wordFreqByPOS['NN'] = {'park': 2, 'review': 1}
depCorrelates = {} # e.g. dep[('in', 'IN', '>', True)] = {'NN': 33, 'NNP': 23}
sentences = []

with open(treeFilename) as treeFile:
	words = []
	deps = {}
	depsByIndex = {}
	for line in treeFile:
		if line.strip() != '':
			splitline = line.strip().split('\t')
			depIndex = int(splitline[0])
			depWord = splitline[2]
			depPOS = splitline[3]
			headIndex = int(splitline[8])
			words.append((depIndex, depWord, depPOS, headIndex))
			insertFreqTable(depWord, freqs)
			insertTable(headIndex, depIndex, depsByIndex)
		else:
			for word in words:
				[depIndex, depWord, depPOS, headIndex] = word
				insert2DFreqTable(depPOS, depWord, wordFreqsByPOS)
				headWord = headPOS = direction = ''
				adj = False
				if headIndex != 0 and abs(headIndex-depIndex) == 1:
					headWord = words[headIndex-1][1]
					headPOS = words[headIndex-1][2]
					if depIndex < headIndex:
						direction = '<'
					else:
						direction = '>'
	
				insert2DFreqTable((headWord, headPOS, direction), depPOS, depCorrelates)
				insertTable((headIndex, headWord, headPOS), (depIndex, depWord, depPOS, direction), deps)
			sentences.append(deps)
			deps = {}
			depsByIndex.clear()
			del words[0:]
treeFile.close()

entropy = 0.0
depEntropy = 0.0
totalTokens = sum(freqs.values())
wordFreqsByPOSTotals = {}
for k in wordFreqsByPOS:
	wordFreqsByPOSTotals[k] = sum(wordFreqsByPOS[k].values())
depCorrelatesTotals = {}
for k in depCorrelates:
	depCorrelatesTotals[k] = sum(depCorrelates[k].values())

for sentence in sentences:
	for head in sentence:
		(headIndex, headWord, headPOS) = head
		for dep in sentence[head]:
			(depIndex, depWord, depPOS, direction) = dep
			pDep = 1.0 * freqs[depWord] / totalTokens
			depGivenPOS = 1.0 * wordFreqsByPOS[depPOS][depWord] / wordFreqsByPOSTotals[depPOS]
			correlates = (headWord, headPOS, direction)
			depPOSGivenCorrelates = 1.0 * depCorrelates[correlates][depPOS] / depCorrelatesTotals[correlates]
			qDep = depGivenPOS * depPOSGivenCorrelates
			selfInfo = -math.log(pDep, 2.0)
			entropy += pDep * selfInfo
			depSelfInfo = -math.log(qDep, 2.0)
			depEntropy += pDep * depSelfInfo

sys.stdout.write('*No dependencies*\n\n')
sys.stdout.write('Entropy: ' + repr(entropy) + ' bits \n')
sys.stdout.write('Entropy per word: ' + repr(entropy/totalTokens) + ' bits \n')
sys.stdout.write('Perplexity per word: ' + repr(pow(2, entropy/totalTokens)) + '\n\n')

sys.stdout.write('*With dependencies (adjacents only)*\n\n')
sys.stdout.write('Cross Entropy: ' + repr(depEntropy) + ' bits \n')
sys.stdout.write('Cross Entropy per word: ' + repr(depEntropy/totalTokens) + ' bits \n')
sys.stdout.write('Perplexity per word: ' + repr(pow(2, depEntropy/totalTokens)) + '\n\n')

sys.stdout.write('Total number of words: ' + repr(totalTokens) + '\n')
