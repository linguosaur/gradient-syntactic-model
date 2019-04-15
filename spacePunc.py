import operator, re, string, sys

# space out punctuation marks
def spacePunc(string):
	splitStr = re.split('([!?\s\,\.\(\);:\'\"])', string)
	splitStr.remove(' ')
	newString = ' '.join(splitStr)
	newString = re.sub('\s{2,}', ' ', newString)
	return newString

textFile = open(sys.argv[1])
textFileLines = textFile.readlines()
textFile.close()

for line in textFileLines:
	print spacePunc(line.decode('utf-8').lower()).encode('utf-8')
