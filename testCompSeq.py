from compareSeqLib import *

sys.stderr.write('reading profiles file . . . ')
profilesFile = open(sys.argv[1])
profilesFileLines = profilesFile.readlines()
profilesFile.close()
sys.stderr.write('done.\n\n')

profiles = {}
contextFreqs = {}
maxSeqLen = 0

fillProfiles(profiles, contextFreqs, profilesFileLines)

sys.stderr.write('finding most similar sequences . . . \n')
numOfSeqs = 180000
seq = 'of the of the'
seq2 = 'in the of the'
for i in range(numOfSeqs):
	if i % 10 == 0:
		sys.stderr.write(repr(i) + ', ')
	for j in range(numOfSeqs-1):
		seqDist = compareSeqInside(seq, seq2, contextFreqs, profiles)
sys.stderr.write('\n')
sys.stderr.write('done.\n\n')
