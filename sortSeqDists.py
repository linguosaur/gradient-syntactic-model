import sys

seqDistFilenames = sys.argv[1:]
filenameSeparator = '-'

sys.stderr.write('Files to sort:\n')
for seqDistFilename in seqDistFilenames:
	sys.stderr.write(seqDistFilename + '\n')
sys.stderr.write('\n')

for seqDistFilename in seqDistFilenames:
	seqDists = []
	
	sys.stderr.write('reading in ' + seqDistFilename + '. . . ')
	with open(seqDistFilename) as seqDistFile:
		for line in seqDistFile:
			[seq1, seq2, dist] = line.strip().split('\t')
			seqDists.append((float(dist), seq1, seq2))
	seqDistFile.close()
	sys.stderr.write('done\n')

	sys.stderr.write('sorting . . . ')
	seqDists.sort()
	sys.stderr.write('done\n')

	splitFilename = seqDistFilename.split(filenameSeparator)
	splitFilename.insert(2, 'sorted')
	outFilename = filenameSeparator.join(splitFilename)

	sys.stderr.write('printing sorted results to file . . . ')
	with open(outFilename, 'w') as outFile:
		for item in seqDists:
			(dist, seq1, seq2) = item
			outFile.write('\t'.join([seq1, seq2, repr(dist)]) + '\n')
	outFile.close()
	sys.stderr.write('done\n')
