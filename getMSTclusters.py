import sys, MinimumSpanningTree

graph = []

# Jaccard distances must be sorted in increasing order
with open(sys.argv[1]) as jdFile:		
	sys.stderr.write('putting sorted edges into a list . . . ')
	for line in jdFile:
		(word1, word2, weight) = line.rstrip().split('\t')
		graph.append((float(weight), word1, word2))
	sys.stderr.write('done.\n\n')
jdFile.close()

sys.stderr.write('running MST . . .')
clusters = MinimumSpanningTree.getMSTClusters(graph)
sys.stderr.write('done.\n\n')

sys.stderr.write('printing clusters . . . ')
for node in clusters:
	sys.stdout.write(seq + ':\n')
	for member in clusters[seq]:
		sys.stdout.write(member[0] + '\t' + repr(member[1]) + '\n')
	sys.stdout.write('\n')
sys.stderr.write('done.\n\n')
