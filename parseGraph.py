import sys
from graphics import *

# To do:
# 1. fix calcPhraseLnHeights() *check!*
# 2. make sure box lines and word lines at the bottom don't overlap *check!*

def drawText():
    for i in range(len(sent)):
        word = sent[i]
        txt = Text(Point(textCols[i],textRow),word)
        txt.setSize(12)
        txt.draw(win)

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# elem1Index and elem2Index are either an int or a 2-ple (a,b), where a < b
# distance > 0 if textCols[elem1] is to the left of textCols[elem2], < 0 otherwise
def distPhrase (elem1Index,elem2Index):
    dist = textCols[elem2Index] - textCols[elem1Index]
    #sys.stderr.write(repr(elem1Index) + ' to ' + repr(elem2Index) + ': ' + repr(dist) + '\n')
    return dist

# entry is either a number or ''
def updateW2WEntryCount(row,col,table,connections):
    if table[row][col] == '': return
    
    if row not in connections:
        connections[row] = {'<':[], '>':[]}
    if col < row:
        connections[row]['<'].append(col)
    else:
        connections[row]['>'].append(col)

    if col not in connections:
        connections[col] = {'<':[], '>':[]}
    if row < col:
        connections[col]['<'].append(row)
    else:
        connections[col]['>'].append(row)

# inserts item into the correct place in a sorted list
def insertItem(item,sortedList):
    i = 0
    while i < len(sortedList) and distPhrase(item,sortedList[i]) <= 0:
        i += 1
    sortedList.insert(i,item)

# entry is either a number or ''
def updatePhraseEntryCount(elem1Index,elem2Index,table,connections):
    if table[elem1Index][elem2Index] == '': return

    if elem1Index not in connections:
        connections[elem1Index] = {'<':[], '>':[]}        
    if elem2Index not in connections:
        connections[elem2Index] = {'<':[], '>':[]}
    if distPhrase(elem1Index,elem2Index) > 0:
        insertItem(elem1Index,connections[elem2Index]['<'])
        insertItem(elem2Index,connections[elem1Index]['>'])
    else:
        insertItem(elem1Index,connections[elem2Index]['>'])
        insertItem(elem2Index,connections[elem1Index]['<'])

def readEntries(table,connections,tableType):
    for elemIndex1 in table:
        for elemIndex2 in table[elemIndex1]:
            if tableType == 'w2w':
                updateW2WEntryCount(elemIndex1,elemIndex2,table,connections)
            elif tableType == 'w2p' or tableType == 'p2p':
                updatePhraseEntryCount(elemIndex1,elemIndex2,table,connections)

# is p1 under p2?
# p1 and p2 are 2-ples (a,b), where a < b
# assume p1 != p2
def isUnder(p1,p2):
    if p1[0] >= p2[0] and p1[1] <= p2[1]:
        return True
    if p1[0] < p2[0] and p1[1] > p2[0] and p1[1] < p2[1]:
        return True
    if p1[0] > p2[0] and p1[0] < p2[1] and p1[1] > p2[1]:
        return True

    return False

def calcWordLnHeights(connections):
    heights = {}
    pairs = []
    for i1 in connections:
        for i2 in connections[i1]['>']:
            pairs.append((i1,i2))
    sortedPairs = sorted(pairs,key=lambda pair: pair[1]-pair[0])
    for pair in sortedPairs:
        unders = [p for p in heights.keys() if isUnder(p,pair)]
        if len(unders) == 0:
            heights[pair] = 1
        else:
            heights[pair] = max(heights[p] for p in unders) + 1
        sys.stderr.write('heights[' + repr(pair) + '] = ' + repr(heights[pair]) + '\n')

    return heights

# elemPair is a 2-ple (a,b), where each element may be an int or a tuple (a,b), where a < b
def getSpan(elemPair):
    return (textCols[elemPair[0]],textCols[elemPair[1]])

def calcPhraseLnHeights(connections):
    heights = {}
    
    # (a,(b,c)), where b < c; or ((a,b),(c,d)), where a < b and c < d
    # first element is always left of second element
    pairs = [] 

    for elem_i in connections:
        for elem_j in connections[elem_i]['>']:
            pairs.append((elem_i,elem_j))

    sortedPairs = sorted(pairs,key=lambda pair: distPhrase(pair[0],pair[1]))
    for pair in sortedPairs:
        unders = [p for p in heights.keys() if isUnder(getSpan(p),getSpan(pair))]
        sys.stderr.write('under ' + repr(pair) + ': ' + repr(unders) + '\n')
        if len(unders) == 0:
            heights[pair] = 1
        else:
            heights[pair] = max(heights[p] for p in unders) + 1
        sys.stderr.write('heights[' + repr(pair) + '] = ' + repr(heights[pair]) + '\n')

    return heights

def drawWord2WordLn(wordIndex1,wordIndex2,cpr,connections,heights):
    connectionOrder1 = connections[wordIndex1]['>'] + connections[wordIndex1]['<']
    connectionOrder2 = connections[wordIndex2]['>'] + connections[wordIndex2]['<']
    offset1 = lnSpacing*((len(connectionOrder1)-1)/2 - connectionOrder1.index(wordIndex2))
    offset2 = lnSpacing*((len(connectionOrder2)-1)/2 - connectionOrder2.index(wordIndex1))
    heightOffset = lnHeightSpacing*heights[(wordIndex1,wordIndex2)]
    if cpr > cprMax:
        cpr = cprMax
    color = int(255.0-255.0*cpr/cprMax)
    
    shortLn1 = Line(Point(textCols[wordIndex1]+offset1,lnBottom),Point(textCols[wordIndex1]+offset1,lnBottom-heightOffset))
    shortLn1.setOutline(color_rgb(color,color,color))
    shortLn1.setWidth(lnWidth)
    shortLn1.draw(win)
    shortLn2 = Line(Point(textCols[wordIndex2]+offset2,lnBottom),Point(textCols[wordIndex2]+offset2,lnBottom-heightOffset))
    shortLn2.setOutline(color_rgb(color,color,color))
    shortLn2.setWidth(lnWidth)
    shortLn2.draw(win)
    ln = Line(Point(textCols[wordIndex1]+offset1,lnBottom-heightOffset),Point(textCols[wordIndex2]+offset2,lnBottom-heightOffset))
    ln.setOutline(color_rgb(color,color,color))
    ln.setWidth(lnWidth)
    ln.draw(win)

def drawWord2WordLns(table,connections,lnHeights):
    for row in range(len(table)):
        sentLength = len(table[row])
        for col in range(sentLength):
            entry = table[row][col]
            if entry != '':
                sys.stderr.write('\t'.join([repr(row),repr(col),repr(entry)]) + '\n')
                drawWord2WordLn(row,col,entry,connections,lnHeights)

def calcPhraseBoxHeights(phraseEndpts):
    heights = {}
    for pair in sorted(phraseEndpts,key=lambda p: p[1]-p[0]):
        unders = [p for p in heights.keys() if isUnder(p,pair)]
        if len(unders) == 0:
            heights[pair] = 1
        else:
            h = 1
            while h in (heights[p] for p in unders):
                h += 1
            heights[pair] = h
        sys.stderr.write('boxHeights[' + repr(pair) + '] = ' + repr(heights[pair]) + '\n')

    return heights

def drawPhraseBox(start,end,boxHeights,boxBottoms,boxSides):
    heightOffset = boxHeights[(start,end)]
    leftOffset = boxWSpacing * len([p for p in boxHeights if p[0] == start and heightOffset > boxHeights[p]])
    rightOffset = boxWSpacing * len([p for p in boxHeights if p[1] == end and heightOffset > boxHeights[p]])
    pt1col = textCols[start]-len(sent[start])*textSize/2-leftOffset
    pt1row = textRow-textSize*1.5-boxHtSpacing*heightOffset
    pt1 = Point(pt1col,pt1row)
    pt2col = textCols[end-1]+len(sent[end-1])*textSize/2+rightOffset
    pt2row = textRow+textSize*1.5+boxHtSpacing*heightOffset
    pt2 = Point(pt2col,pt2row)
    rect = Rectangle(pt1,pt2)
    rect.draw(win)

    boxBottoms[(start,end)] = pt2row
    boxSides.append(pt1col)
    boxSides.append(pt2col)

    sys.stderr.write(repr((start,end)) + ': ')
    sys.stderr.write('leftOffset = ' + repr(leftOffset) + '\t')
    sys.stderr.write('rightOffset = ' + repr(rightOffset) + '\n')

def drawPhraseLn(elem1Index,elem2Index,table,connections,heights):
    cpr = table[elem1Index][elem2Index]
    connectionOrder1 = connections[elem1Index]['>'] + connections[elem1Index]['<']
    connectionOrder2 = connections[elem2Index]['>'] + connections[elem2Index]['<']
    offset1 = lnSpacing*((len(connectionOrder1)-1)/2 - connectionOrder1.index(elem2Index))
    offset2 = lnSpacing*((len(connectionOrder2)-1)/2 - connectionOrder2.index(elem1Index))
    if (elem1Index,elem2Index) in heights:
        heightOffset = lnHeightSpacing*heights[(elem1Index,elem2Index)]
    else:
        heightOffset = lnHeightSpacing*heights[(elem2Index,elem1Index)]
    if cpr > cprMax:
        cpr = cprMax
    color = int(255.0-255.0*cpr/cprMax)

    virtualLnTop = textRow+textToLnEdges
    [lnTop1,lnTop2] = [lnTop,lnTop]
    if isinstance(elem1Index,tuple):
        lnTop1 = phraseBoxBottoms[elem1Index]
    if isinstance(elem2Index,tuple):
        lnTop2 = phraseBoxBottoms[elem2Index]

    shortLn1 = Line(Point(textCols[elem1Index]+offset1,lnTop1),Point(textCols[elem1Index]+offset1,virtualLnTop+heightOffset))
    shortLn1.setOutline(color_rgb(color,color,color))
    shortLn1.setWidth(lnWidth)
    shortLn1.draw(win)
    shortLn2 = Line(Point(textCols[elem2Index]+offset2,lnTop2),Point(textCols[elem2Index]+offset2,virtualLnTop+heightOffset))
    shortLn2.setOutline(color_rgb(color,color,color))
    shortLn2.setWidth(lnWidth)
    shortLn2.draw(win)
    ln = Line(Point(textCols[elem1Index]+offset1,virtualLnTop+heightOffset),Point(textCols[elem2Index]+offset2,virtualLnTop+heightOffset))
    ln.setOutline(color_rgb(color,color,color))
    ln.setWidth(lnWidth)
    ln.draw(win)

def drawPhraseLns(table,connections,lnHeights):
    for elem1Index in table:
        for elem2Index in table[elem1Index]:
            entry = table[elem1Index][elem2Index]
            if entry != '':
                #sys.stderr.write('\t'.join([repr(elem1Index),repr(elem2Index),repr(entry)]) + '\n')
                drawPhraseLn(elem1Index,elem2Index,table,connections,lnHeights)

# translates indices of phrases from row/col to phraseEndpts[row/col]
def translateTableIndices(table,tableType):
    newTable = {}
    for row in range(len(table)):
        newRow = row
        if tableType == 'w2w' or tableType == 'w2p':
            newTable[row] = {}
        elif tableType == 'p2p':
            newRow = phraseEndpts[row]
            newTable[newRow] = {}
        for col in range(len(table[row])):
            newCol = col
            if tableType == 'w2p' or tableType == 'p2p':
                newCol = phraseEndpts[col]
            newTable[newRow][newCol] = table[row][col]

    return newTable

def calcTextCols(phraseEndpts,boxSides):
    for p in phraseEndpts:
        textCol = (textCols[p[0]]+textCols[p[1]-1])/2
        if textCol in textCols.values() or [s for s in boxSides if abs(textCol-s) <= 2*lnWidth]:
            textCols[p] = textCol+winCols/(8*len(sent))
        else:
            textCols[p] = textCol
        sys.stderr.write('\t'.join([repr(p),repr(textCols[p])]) + '\n')
    

logFileName = '..\output\sent2-PMI-discrete.txt'
parseFileName = '..\output\sent2-parse-discrete.txt'

tables = []
sent = ''
cprMax = 5.0 # too low?
with open(logFileName) as logFile:
    table = []
    firstLine = True
    for line in logFile:
        splitLine = line.rstrip().split('\t')
        if firstLine:
            sent = splitLine[1:]
            firstLine = False
        if len(splitLine) > 0 and splitLine[0] == '': # heading line
            if len(table) > 0:
                tables.append(table)
            table = []
        else:
            newSplitLine = []
            for entry in splitLine[1:]:
                if isNumber(entry):
                    newSplitLine.append(float(entry))
                else:
                    newSplitLine.append('')
            table.append(newSplitLine)

sys.stderr.write('# of tables: ' + repr(len(tables)) + '\n')

phraseEndpts = []
with open(parseFileName) as parseFile:
    for line in parseFile:
        splitLine = line.split('\t')
        sys.stderr.write(repr(splitLine) + '\n')
        if len(splitLine) == 3:
            indices = splitLine[0][1:-1].split(',')
            indices = tuple([int(i) for i in indices])
            phraseEndpts.append(indices)
            sys.stderr.write(repr(indices) + '\n')

winCols = len(sent)*90
winRows = 400
textCols = {}
textRow = winRows/2
textSize = 12
textToLnEdges = 50
lnBottom = textRow-textToLnEdges
lnTop = textRow+textSize*1.2
lnHeightSpacing = 10
lnWidth = 2
lnSpacing = 3
boxHtSpacing = 5
boxWSpacing = 3
[w2wNconnections,wp2pNconnections] = [{},{}]
lnHeights = {}

win = GraphWin("My Window",winCols+50,winRows)
win.setBackground(color_rgb(255,255,255))

[w2wNtable,p2pNtable,w2pNtable] = [tables[2],tables[5],tables[9]]

for i in range(len(sent)):
    textCols[i] = (i+0.5)*winCols/len(sent)
    sys.stderr.write('\t'.join([repr(i),repr(textCols[i])]) + '\n')
drawText()
w2wNtableTranslated = translateTableIndices(w2wNtable,'w2w')
readEntries(w2wNtableTranslated,w2wNconnections,'w2w')
w2wNlnHeights = calcWordLnHeights(w2wNconnections)
drawWord2WordLns(w2wNtableTranslated,w2wNconnections,w2wNlnHeights)

for elem1 in w2wNconnections:
    for dir in w2wNconnections[elem1]:
        sys.stderr.write('w2wNconnections[' + repr(elem1) + '][' + repr(dir) + ']: ' + repr(w2wNconnections[elem1][dir]) + '\n')
            
if len(phraseEndpts) > 0:
    phraseBoxHeights = calcPhraseBoxHeights(phraseEndpts)
    phraseBoxBottoms = {}
    phraseBoxSides = []
    for indexPair in phraseEndpts:
        (start,end) = indexPair
        drawPhraseBox(start,end,phraseBoxHeights,phraseBoxBottoms,phraseBoxSides)

    w2pNtableTranslated = translateTableIndices(w2pNtable,'w2p')
    p2pNtableTranslated = translateTableIndices(p2pNtable,'p2p')

    textCol = calcTextCols(phraseEndpts,phraseBoxSides)
    
    readEntries(w2pNtableTranslated,wp2pNconnections,'w2p')
    readEntries(p2pNtableTranslated,wp2pNconnections,'p2p')
    phraseLnHeights = calcPhraseLnHeights(wp2pNconnections)

    for elem1 in wp2pNconnections:
        for dir in wp2pNconnections[elem1]:
            sys.stderr.write('wp2pNconnections[' + repr(elem1) + '][' + repr(dir) + ']: ' + repr(wp2pNconnections[elem1][dir]) + '\n')

    drawPhraseLns(w2pNtableTranslated,wp2pNconnections,phraseLnHeights)
    drawPhraseLns(p2pNtableTranslated,wp2pNconnections,phraseLnHeights)
