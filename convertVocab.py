import sys

jdFile = open(sys.argv[1])
jdFileLines = jdFile.readlines()
jdFile.close()

dicFile = open(sys.argv[2])
dicFileLines = dicFile.readlines()
dicFile.close()

dic = {}
for line in dicFileLines:
	splitLine = line.strip().split('\t')
	dic[splitLine[1]] = int(splitLine[0])

sys.stderr.write('number of words in dic: ' + repr(len(dic)) + '\n')

i = 0
for line in jdFileLines:
	if i % 1000000 == 0:
		sys.stderr.write(repr(i/1000000) + ', ')
	i += 1
	splitLine = line.strip().split('\t')
	if (len(splitLine)) == 3:
		word1 = splitLine[0]
		word2 = splitLine[1]
		dist = splitLine[2]
	sys.stdout.write(repr(dic[word1]) + '\t' + repr(dic[word2]) + '\t' + dist + '\n')
sys.stderr.write('\n')
