import sys
import findsimilarwordslib
import compareSeqLib

sys.stderr.write('reading profiles file . . . ')
profilesFile = open(sys.argv[1])
profilesFileLines = profilesFile.readlines()
profilesFile.close()
sys.stderr.write('done.\n\n')

profiles = {}
patternTypeFreqs = {}

findsimilarwordslib.fillProfiles(profiles, profilesFileLines)

sys.stderr.write('len(profiles): ' + repr(len(profiles)) + '\n')
while True:
	sys.stdout.write('sequence 1: ')
	seq1 = sys.stdin.readline().strip().split()

	sys.stdout.write('sequence 2: ')
	seq2 = sys.stdin.readline().strip().split()

	sys.stdout.write('sequence similarity: ' + repr(compareSeqLib.compareSeqInside(seq1, seq2, profiles)) + '\n\n')
