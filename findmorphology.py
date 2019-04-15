import codecs, operator, sys

textfile = codecs.open(sys.argv[1], encoding='latin-1')
wordset = set()
root = 'kansa'
for line in textfile:
	splitLine = line.strip().split()
	for word in splitLine:
		if word.startswith(root):
			wordset.add(word)

for w in sorted(wordset, key=operator.itemgetter(0)):
	print w.encode('latin-1')
