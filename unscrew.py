import sys

jdFile = open(sys.argv[1])
jdFileLines = jdFile.readlines()
jdFile.close()

headword = ''
for line in jdFileLines:
	splitLine = line.strip().split('\t')
	if len(splitLine) == 3:
		word1 = splitLine[0]
		word2 = splitLine[1]
		dist = splitLine[2]
	if headword != word1:
		sys.stdout.write(word1 + '\t' + word1 + '\t' + '0.0\n')
		headword = word1

	sys.stdout.write(line)
