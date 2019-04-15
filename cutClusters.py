import sys, MinimumSpanningTree


children = {}
maxTimeTick = 0

with open(sys.argv[1]) as clusterFile:
	label = ''
	isReading = False
	for line in clusterFile:
		line = line.rstrip()
		if line == '':
			isReading = False
		elif line[-1] == ':':
			label = line[:-1]
			children[label] = []
			isReading = True
		elif isReading:
			splitLine = line.split('\t')
			if len(splitLine) == 2:
				word = splitLine[0]
				timeTick = int(splitLine[1])
				children[label].append((word, timeTick))
				maxTimeTick = max(timeTick, maxTimeTick)
clusterFile.close()

parents = MinimumSpanningTree.constructParents(children)

sys.stdout.write('Number of words: ' + repr(len(children)) + '\n')
sys.stdout.write('Last time tick: ' + repr(maxTimeTick) + '\n\n')

threshSwitch = '--thresh'
firstNSwitch = '--firstN'
switch = threshSwitch
if len(sys.argv) >= 3:
	switch = sys.argv[2]

while True:
	sys.stdout.write('word: ')
	queryWord = sys.stdin.readline().strip()

	if switch == threshSwitch:
		sys.stdout.write('time threshold: ')
		timeThresh = int(sys.stdin.readline().strip())
		sys.stdout.write('\n')
	
		cluster = MinimumSpanningTree.getClusterByThresh(queryWord, timeThresh, children, parents)
		for word, time in cluster:
			sys.stdout.write(word + '\t' + repr(time) + '\n')
	
		sys.stdout.write('\n')
	elif switch == firstNSwitch:
		sys.stdout.write('N: ')
		n = int(sys.stdin.readline().strip())

		cluster = MinimumSpanningTree.getFirstNCluster(queryWord, n, children, parents)
		for word, time in cluster:
			sys.stdout.write(word + '\t' + repr(time) + '\n')
	
		sys.stdout.write('\n')
