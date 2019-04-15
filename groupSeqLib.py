def encodeSeq(seqText, dic):
    splitSeqCode = seqText.split()
    for i in range(len(splitSeqCode)):
        splitSeqCode[i] = dic[splitSeqCode[i]]

    return tuple(splitSeqCode)

# seqCode is a tuple of word indices, as given by dic
def decodeSeq(seqCode, reverseDic):
    splitSeqText = list(seqCode)
    for i in range(len(splitSeqText)):
        splitSeqText[i] = reverseDic[splitSeqText[i]]

    return ' '.join(splitSeqText)

def insert2D(key1, key2, dist, table):
    if key1 not in table:
        table[key1] = {}
    if key2 not in table:
        table[key2] = {}

    table[key1][key2] = dist
    table[key2][key1] = dist

    return
