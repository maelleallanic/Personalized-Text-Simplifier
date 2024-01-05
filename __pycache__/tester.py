currWord = 'fried'
print("started")
for i in range(0, len(currWord)):
    # print(currWord[i:])
    # print(dictCommonEndingsCurrTense)
    compareWord = 'disgusted'
    lenDiff = len(compareWord) - len(currWord[i:])
    print(lenDiff)
    if( lenDiff >= 0):
        print(compareWord[lenDiff:])
        print(currWord[i:])
        if compareWord[lenDiff:] == currWord[i:]:
            print("FOUND MATCH")

            