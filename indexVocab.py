import sys

profilesFile = open(sys.argv[1])
profilesFileLines = profilesFile.readlines()
profilesFile.close()

words = []
heading = ''
for line in profilesFileLines:
	line = line.rstrip()
	if line != '' and line[-1] == ':':
		heading = line[:-1]
		words.append(heading)

words.sort()
sys.stderr.write('number of words, sorted: ' + repr(len(words)) + '\n')

for index in range(len(words)):
	sys.stdout.write(repr(index) + '\t' + words[index] + '\n')
