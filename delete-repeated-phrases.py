import sys

sentFileName = sys.argv[1]

seen = []
with open(sentFileName) as sentFile:
	for line in sentFile:
		phrase = line.strip()
		if phrase not in seen:
			seen.append(phrase)

for phrase in seen:
	sys.stdout.write(phrase + '\n')
