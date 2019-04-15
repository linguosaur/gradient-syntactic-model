import sys

parseFileName = sys.argv[1]

with open(parseFileName) as parseFile:
	for line in parseFile:
		splitLine = line.split('\t')
		if len(splitLine) == 3:
			phrase = splitLine[1]
			sys.stdout.write(phrase + '\n')
