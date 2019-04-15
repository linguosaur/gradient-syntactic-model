"""UnionFind.py

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with significant additional changes by D. Eppstein.
"""
import sys

class UnionFind:
	"""Union-find data structure.

	Each unionFind instance X maintains a family of disjoint sets of
	hashable objects, supporting the following two methods:

	- X[item] returns a name for the set containing the given item.
	Each set is named by an arbitrarily-chosen one of its members; as
	long as the set remains unchanged it will keep the same name. If
	the item is not yet part of a set in X, a new singleton set is
	created for it.

	- X.union(item1, item2, ...) merges the sets containing each item
	into a single larger set.  If any item is not yet part of a set
	in X, it is added to X as one of the members of the merged set.

	Modified by Simon Fung, May 2015.
	"""

	def __init__(self, G):
		"""Create a new empty union-find structure."""
		self.weights = {}
		self.parents = {} # a dictionary of objects
		self.children = {} # a dictionary of lists of tuples of the form (object, self.timesMerged)
		self.timesMerged = 0
		for W,u,v in G:
			if u not in self.weights:
				self.weights[u] = 1
				self.parents[u] = u
				self.children[u] = [(u, self.timesMerged)]
			if v not in self.weights:
				self.weights[v] = 1
				self.parents[v] = v
				self.children[v] = [(v, self.timesMerged)]

	def __getitem__(self, object):
		"""Find and return the name of the set containing the object."""

		# check for previously unknown object
		if object not in self.parents:
			self.parents[object] = object
			self.children[object] = [(object, self.timesMerged)]
			self.weights[object] = 1
			return object
		
		return self.parents[object]

	def __iter__(self):
		"""Iterate through all items ever found or unioned by this structure."""
		return iter(self.parents)

	def union(self, *objects):
		parentsChanged = False

		"""Find the sets containing the objects and merge them all."""
		roots = [self[x] for x in objects]
		heaviest = max([(self.weights[r],r) for r in roots])[1]

		for r in roots:
			if r != heaviest:
				if not parentsChanged: # should only happen once per function call
					parentsChanged = True
					self.timesMerged += 1
				self.weights[heaviest] += self.weights[r]
				for child in self.children[r]:
					self.parents[child[0]] = heaviest
					self.children[heaviest].append((child[0], self.timesMerged))

	def getParents(self):
		return self.parents
	
	def getChildren(self):
		return self.children
