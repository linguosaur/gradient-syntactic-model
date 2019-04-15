import re, sys

chunksfile = open(sys.argv[1])
chunksfileLines = chunksfile.readlines()
chunksfile.close()

queryWord = 'agency'

for line in chunksfileLines:
	if re.search('^[\w\d$%].* ' + queryWord + '\t', line) != None:
#	if re.search('^' + queryWord + ' [\w\d$%]*\t', line) != None:
		print line.strip()
