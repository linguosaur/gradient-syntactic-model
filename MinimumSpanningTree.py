"""MinimumSpanningTree.py

Kruskal's algorithm for minimum spanning trees. D. Eppstein, April 2006.
Modified by Simon Fung, May 2015.
"""
import sys
from UnionFind import UnionFind

def getMSTChildren(G):
	"""
	Returns a dictionary D where each entry is a node x in an undirected graph G, 
	and x is the representative node for the clique it belongs to, at various
	points in time during Kruskal's algorithm. D[x] is a list of tuples, (y, t),
	where y is a node in the same clique as x (and may be x itself), at time t.
	G is given as a list of edges, sorted in increasing order by weight.
	Each edge is a 3-element tuple, in the form (W, u, v), where u and v
	are the vertices, and W is the weight of the edge between them.
	"""

	# Kruskal's algorithm: sort edges by weight, and add them one at a time.
	# We use Kruskal's algorithm, first because it is very simple to
	# implement once UnionFind exists, and second, because the only slow
	# part (the sort) is sped up by being built in to Python.
	subtrees = UnionFind(G)
	i = 0
	for W,u,v in G:
		if i % 1000 == 0:
			sys.stderr.write(repr(i/1000) + ', ')
		i += 1

		if subtrees[u] != subtrees[v]:
			subtrees.union(u,v)

	return subtrees.getChildren()

def constructParents(children):
	parents = {}

	for label in children:
		for child, t in children[label]:
			if child not in parents:
				parents[child] = []
			parents[child].append((label, t))

	for child in parents:
		parents[child].sort(key=lambda pair:pair[1])

	return parents

# returns a list of tuples, (x, timeJoined), where
# x is an element in the clique of *word* that joined at *timeJoined*, and
# where *timeJoined* < *timeThresh*.
def getClusterByThresh(word, timeThresh, children, parents):
	cluster = []

	for currentLabel, timeJoined in parents[word]:
		if timeThresh < timeJoined:
			break
		currentChildren = children[currentLabel]
		clusteredWords = [w for w, t in cluster]
		for w, t in currentChildren:
			if t <= timeThresh and w not in clusteredWords:
				if timeJoined >= t:
					cluster.append((w, timeJoined))
				else:
					cluster.append((w, t))

	return cluster

def getFirstNCluster(word, n, children, parents):
	cluster = []

	for currentLabel, timeJoined in parents[word]:
		currentChildren = children[currentLabel]
		clusteredWords = [w for w, t in cluster]
		for w, t in currentChildren:
			if len(cluster) < n:
				if w not in clusteredWords:
					if timeJoined >= t:
						cluster.append((w, timeJoined))
					else:
						cluster.append((w, t))
			else:
				return cluster

	return cluster


# If run standalone, perform a test
if __name__ == "__main__":
	"""Check that MinimumSpanningTree returns the correct answer.
	T = [(2,3),(0,1),(0,3)]"""

	G = [(10, 2, 3), (11, 0, 1), (12, 0, 3), (13, 0, 2), (14, 1, 3)]

	children = getMSTChildren(G)
	sys.stdout.write('children:\n')
	for label in children:
		sys.stdout.write(repr(label) + ': ' + repr(children[label]) + '\n')
	sys.stdout.write('\n')

	parents = constructParents(children)
	sys.stdout.write('parents:\n')
	for node in parents:
		sys.stdout.write(repr(node) + ': ' + repr(parents[node]) + '\n')
	sys.stdout.write('\n')

	queryWord = 3
	timeThresh = 1
	testCluster = getCluster(queryWord, timeThresh, children, parents)

	sys.stdout.write('cluster for ' + repr(queryWord) + ' and timeThresh ' + repr(timeThresh) + ':\n')
	for word, time in testCluster:
		sys.stdout.write(repr(word) + '\t' + repr(time) + '\n')
