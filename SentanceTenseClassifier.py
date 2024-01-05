import nltk
from nltk.corpus import wordnet

#I adapted the Naive Bayes Algorythm
#Video I used to undestand the algorythm https://www.youtube.com/watch?v=O2L2Uv9pdDA
#I adapted it to find verb endings for tenses

class SentanceTenseClassifier:
    def __init__(self):
        self.tenseCategories = ["past", "present", "future"]
        self.pastHistogram = dict()
        self.presentHistogram = dict()
        self.futureHistogram = dict()

        self.listOfTensesHistograms = \
            [self.pastHistogram, 
            self.presentHistogram, 
            self.futureHistogram]

        self.totalNumberOfWordsInPastSentences = 0
        self.totalNumberOfWordsInPresentSentences = 0
        self.totalNumberOfWordsInPastSentences = 0
        self.listOfTotalNumberOfWordsInTenseSentences = \
            [self.totalNumberOfWordsInPastSentences, 
            self.totalNumberOfWordsInPresentSentences, 
            self.totalNumberOfWordsInPastSentences]
        
        self.commonEndingsInPast = dict()
        self.commonEndingsInPresent = dict()
        self.commonEndingsInFuture = dict()
        self.listOfDictCommonEndingsInTenses = \
            [self.commonEndingsInPast, 
            self.commonEndingsInPresent, 
            self.commonEndingsInFuture]


        self.pastEndingsProbablilities = dict()
        self.presentEndingsProbablilities = dict()
        self.futureEndingsProbablilities = dict()
        self.listOfEndingsProbablitiesDict = \
            [self.pastEndingsProbablilities, 
            self.presentEndingsProbablilities, 
            self.futureEndingsProbablilities]

        self.significantCommonEndingsProbablilitiesInPast = dict()
        self.significantCommonEndingsProbablilitiesInPresent = dict()
        self.significantCommonEndingsProbablilitiesInFuture = dict()
        self.listOfDictSignificantCommonEndingsProbablilitiesInTenses = \
            [self.significantCommonEndingsProbablilitiesInPast, 
            self.significantCommonEndingsProbablilitiesInPresent, 
            self.significantCommonEndingsProbablilitiesInFuture]

        self.allItendifiedVerbEndings = set()

        self.commonWordsThatArentVerbs = set()

        self.IrregularPastVerbs = set()


    def train(self, trainFileName, commonWordsThatArentVerbsFileName):
        # We'll start you off with the code to read a file
        # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
        # (The UTF-8 encoding helps work on all operating systems)
        with open(trainFileName, "r", encoding="utf-8") as f:
            fileString = f.read()
        # Parse the file data and load into a dictionary (rather than just 
        # printing it)
        firstLine = True
        for line in fileString.splitlines(): 
            #goes through every line and adds it to the dictionary
            if firstLine:
                print('HEADER LINE: ', end='')
                firstLine = False
            else:
                splitedLine = line.split(',,')
                sentance = splitedLine[0]
                tense = splitedLine[1]

                if ( tense == 'past'):
                    tenseIndex = 0
                elif (tense == 'present'):
                    tenseIndex = 1
                else:
                    tenseIndex = 2

                #want to just get the words
                sentance = sentance.replace(",", "")
                sentance = sentance.replace("'s", "s")
                sentance = sentance.replace("'", "")
                sentance = sentance.replace(".", "")
                sentance = sentance.replace('"', "")
                sentance = sentance.lower()

                #counts the words of a tense and adds them to the tense histogram
                for word in sentance.split(" "):
                    self.listOfTotalNumberOfWordsInTenseSentences[tenseIndex] = \
                        self.listOfTotalNumberOfWordsInTenseSentences[tenseIndex] + 1

                    if( word in self.listOfTensesHistograms[tenseIndex]):
                        self.listOfTensesHistograms[tenseIndex][word] = \
                            self.listOfTensesHistograms[tenseIndex][word] + 1
                    else:
                        self.listOfTensesHistograms[tenseIndex][word] = 1
        

        with open(commonWordsThatArentVerbsFileName, "r", encoding="utf-8") as f:
            fileString = f.read()
        # Parse the file data and load into a dictionary (rather than just 
        # printing it)
        firstLine = True
        for word in fileString.splitlines(): 
            #goes through every line and adds it to the dictionary
            if firstLine:
                print('HEADER LINE: ', end='')
                firstLine = False
            else:
                self.commonWordsThatArentVerbs.add(word)


        with open("IrregularVerbs.csv", "r", encoding="utf-8") as f:
            fileString = f.read()
        # Parse the file data and load into a dictionary (rather than just 
        # printing it)
        firstLine = True
        for word in fileString.splitlines(): 
            #goes through every line and adds it to the dictionary
            if firstLine:
                print('HEADER LINE: ', end='')
                firstLine = False
            else:
                self.IrregularPastVerbs.add(word)



        #finds the endings/substrings of words that apprear often
        #ignoring words that arent verbs (csv)
        for tenseIndex in range(0, 3):
            tenseHistogram = self.listOfTensesHistograms[tenseIndex]
            dictCommonEndingsCurrTense = self.listOfDictCommonEndingsInTenses[tenseIndex]
            for currWord in tenseHistogram:

                if currWord not in self.commonWordsThatArentVerbs:
                    for i in range(0, len(currWord)-1): #want to ignore single letters

                        if( currWord[i:] not in dictCommonEndingsCurrTense):

                            for compareWord in tenseHistogram:
                                if compareWord not in self.commonWordsThatArentVerbs:
                                    if( compareWord != currWord):
                                        lenDiff = len(compareWord) - len(currWord[i:])
                                        if( lenDiff >= 0):
                                            
                                            if compareWord[lenDiff:] == currWord[i:]:
                                                #found a match!!
                                                if( currWord[i:] not in 
                                                self.listOfDictCommonEndingsInTenses[tenseIndex]):
                                                    dictCommonEndingsCurrTense[currWord[i:]] \
                                                        = tenseHistogram[currWord]
                                                
                                                dictCommonEndingsCurrTense[currWord[i:]] = \
                                                    dictCommonEndingsCurrTense[currWord[i:]] + \
                                                        tenseHistogram[compareWord]

        #adding words that appread multiple times because the whole word could be a verb
        #and ignorning words that arent verbs (csv)
        for tenseIndex in range(0, 3): 
            tenseHistogram = self.listOfTensesHistograms[tenseIndex]
            dictCommonEndingsCurrTense = self.listOfDictCommonEndingsInTenses[tenseIndex]
            for currWord in tenseHistogram:
                if currWord not in self.commonWordsThatArentVerbs:
                    if tenseHistogram[currWord] > 1:
                        if ( currWord  in dictCommonEndingsCurrTense):
                            dictCommonEndingsCurrTense[currWord] = \
                                dictCommonEndingsCurrTense[currWord] + tenseHistogram[currWord]
                        else:
                            dictCommonEndingsCurrTense[currWord] = tenseHistogram[currWord]


        #calculating probablilites for each ending
        for tenseIndex in range(0, 3): 
            totalNumOfWords = self.listOfTotalNumberOfWordsInTenseSentences[tenseIndex]
            dictCommonEndingsCurrTense = self.listOfDictCommonEndingsInTenses[tenseIndex]
            endingsProbablitiesDict = self.listOfEndingsProbablitiesDict[tenseIndex]

            for word in dictCommonEndingsCurrTense:
                endingsProbablitiesDict[word] = dictCommonEndingsCurrTense[word] / totalNumOfWords
        


        #only keeping the significant endings
        for tenseIndex in range( 0, 3):
            endingsProbablitiesDict = self.listOfEndingsProbablitiesDict[tenseIndex]
            dictSignigicantEndingsProbablilitiesCurrTense = \
                self.listOfDictSignificantCommonEndingsProbablilitiesInTenses[tenseIndex]
            for ending in endingsProbablitiesDict:
                if( endingsProbablitiesDict[ending] >= 0.01):
                    dictSignigicantEndingsProbablilitiesCurrTense[ending] = \
                        endingsProbablitiesDict[ending]

                    self.allItendifiedVerbEndings.add(ending) 

    
    #takes in a sentance and guesses the tense
    def guess(self, sentance):
        
        sentance = sentance.replace(",", "")
        sentance = sentance.replace("'s", "s")
        sentance = sentance.replace("'", "")
        sentance = sentance.replace(".", "")
        sentance = sentance.replace('"', "")
        sentance = sentance.lower()

        probablitySentanceIsPastTense = 0
        probablitySentanceIsPresentTense = 0
        probablitySentanceIsFutureTense = 0
        probablityOfTensesList = \
            [probablitySentanceIsPastTense, 
        probablitySentanceIsPresentTense, 
        probablitySentanceIsFutureTense]

        #calculating the probablilty for each tense
        for tenseIndex in range(0, 3):
            
            
            significantEndingsProbablitiesDict = \
                self.listOfDictSignificantCommonEndingsProbablilitiesInTenses[tenseIndex]

            currProbablility = 1
            for word in sentance.split(" "):
                
                if ( tenseIndex == 0):
                    if word in self.IrregularPastVerbs :

                        return "past"

                
                selectedEnding = "" 
                for ending in self.allItendifiedVerbEndings: #fining longestEnding that works for the word
                    lengthEnding = len(ending)
                    if word[len(word)-lengthEnding:] == ending:
                        if len(ending) > len(selectedEnding):
                            selectedEnding = ending


                    


                
                if( selectedEnding != ""): #getting probabiliy of the longestEndign

                    if( selectedEnding in significantEndingsProbablitiesDict):
                        currProbablility = currProbablility * significantEndingsProbablitiesDict[selectedEnding]

                    else:
                        currProbablility = 0

            #final probablilty
            probablityOfTensesList[tenseIndex] = currProbablility


        #####all possible results
        if(probablityOfTensesList[0] == 1 
        and probablityOfTensesList[1] == 1 
        and probablityOfTensesList[2] == 1):
            return "no verb was identified in the sentence"

        currmax = 0
        probablilityIndexMax = -1

        for i in range(0, 3):
            if probablityOfTensesList[i] > currmax:
                probablilityIndexMax = i
                currmax = probablityOfTensesList[i] 

        if(probablilityIndexMax == -1 ):
            return "all verb tenses probablilities were set to zero"
        else:

            return self.tenseCategories[probablilityIndexMax]
    
    #checks if a word is a verb
    def isVerb(self, word):
        selectedEnding = "" 
        if word in self.IrregularPastVerbs:
            return True
        for ending in self.allItendifiedVerbEndings: #fining longestEnding that works for the word
            lengthEnding = len(ending)
            if word[len(word)-lengthEnding:] == ending:
                if len(ending) > len(selectedEnding):
                    selectedEnding = ending

        if( selectedEnding == ""):
            return False
        else:
            return True


# print(sentanceTenseClassifier.guess("She was opening the letter, she broke into tears."))
# sentance from https://englishgrammarsoft.com/examples-of-tenses-sentences-of-all-tenses/


