import sys

def matchProfiles(word1, word2):
	set1 = profiles[word1]
	set2 = profiles[word2]
	return set1 & set2

sys.stderr.write('reading profiles file . . . ')
profilesFile = open(sys.argv[1])
profilesFileLines = profilesFile.readlines()
profilesFile.close()
sys.stderr.write('done.\n')

profiles = {}

heading = ''
isReading = False
for line in profilesFileLines:
	line = line.rstrip()
	if line == '':
		isReading = False
	elif line[-1] == ':':
		heading = line[:-1]
		profiles[heading] = set()
		isReading = True
	elif isReading:
		profiles[heading].add(line)
		

while True:
	sys.stdout.write('\nfirst word: ')
	heading1 = sys.stdin.readline().rstrip()
	sys.stdout.write('second word: ')
	heading2 = sys.stdin.readline().rstrip()
	commonPatterns = matchProfiles(heading1, heading2)
	sys.stdout.write('\ncommon patterns for ' + heading1 + ' and ' + heading2 + ':\n')
	for pattern in commonPatterns:
		sys.stdout.write(pattern + '\n')
	sys.stdout.write('\nTotal patterns shared: ' + repr(len(commonPatterns)) + '\n')
