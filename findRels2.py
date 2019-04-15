import sys, findsimilarwordslib

textFile = open(sys.argv[1])
textLines = textFile.readlines()
textFile.close()

profileFile = open(sys.argv[2])
profileLines = profileFile.readlines()
profileFile.close()

profiles = {}
findsimilarwordslib.fillProfiles(profiles, profilesFileLines)


