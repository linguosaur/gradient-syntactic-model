import re, sys, operator


wordlistFile = open(sys.argv[1])
compound = {}

sys.stderr.write('reading word list . . . ')
for line in wordlistFile:
	word = line.rstrip()
	if word not in compound:
		compound[word] = []
sys.stderr.write('done\n')

sys.stderr.write('searching for compounds . . . \n')
for word in compound:
	char_i = 1
	while char_i < len(word):
		if word[:char_i] in compound and word[char_i:] in compound:
			compound[word].append(word[:char_i] + '|' + word[char_i:])
		char_i += 1

for k, v in sorted(compound.iteritems()):
	if v == '':
		print k
	else:
		print k + ': ' + '    '.join(v)
