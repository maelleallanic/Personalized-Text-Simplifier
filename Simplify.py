from nltk.corpus import wordnet
from SentanceTenseClassifier import *

#takes in a list of words and the words you want to replace
#returns a string
def replaceWordInSentance(listOfOrigWords, oldWord, newWord):
    #won't work if there is the same verb multiple times
    string = ""
    for word in listOfOrigWords:
        if ( word == oldWord):
            string = string + " " + newWord
        else:
            string = string + " " + word

    return string.strip()
#creates a sentance for a list of strings
def makeSentance(listOfOrigWords):
    string = ""
    for word in listOfOrigWords:
            string = string + " " + word

    return string.strip()

#checks if word contains similar letters
def containsSimilarLetters(word):
    #info from https://www.improvedyslexia.com/explaining-the-dyslexia-alphabet/
    # and from https://www.dyslexia.com/question/what-dyslexics-see/
    s = set()
    for i in word:
        s.add(i)
    if 'b' in s and 'd' in s:
        return True
    elif 'm' in s and 'w' in s:
        return True
    elif 'p' in s and 'q' in s:
        return True
    elif 'b' in s and 'p' in s:
        return True
    elif 'd' in s and 'q' in s:
        return True
    elif 'n' in s and 'z' in s:
        return True
    return False

#checks if word has a lot of the same letters as common words
def hasSameSequence(word, app):
    for freqWord in app.freqWordDict:
        counter = 0
        for i in range(0, len(word)):
            letter = word[i:i+1]
            if ( freqWord.contains(letter)):
                counter = counter + 1
        if counter >= 5 and counter >= len(word)/2:
            return True
    return False





    
    

def hasMultipleDefinitions(word):
    #gets the definition of the selected word 
    # help from https://www.datasciencelearner.com
    #/how-to-get-synonyms-and-antonyms-using-python-nltk/

    syn = wordnet.synsets(word) 
    if len(syn) > 1:
        return True
    return False

    

#gets the csv file name and returns a dictionary of the common words
def loadFreqWordsData(filename, app):
    # We'll start you off with the code to read a file
    # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    # (The UTF-8 encoding helps work on all operating systems)
    with open(filename, "r", encoding="utf-8") as f:
        fileString = f.read()

    # Parse the file data and load into a dictionary (rather than just 
    # printing it)
    firstLine = True
    dictionary = dict()
    for line in fileString.splitlines(): 
        #goes through every line and adds it to the dictionary
        if firstLine:
            print('HEADER LINE: ', end='')
            firstLine = False
        else:
            splitedLine = line.split(',')
            rank = splitedLine[0]
            word = splitedLine[1]
            word = word.replace("'s", "s")
            word = word.replace("'", "")
            word = word.lower()

            dictionary[word] = rank
    app.freqWordDictLastIndex = int(rank)
    return dictionary 

#gets a set of synonyms and returns the simplest one
#based on its ranking in the dictionary
def getSimplestSynonym(origWord, listSyn, app, isVerb):
    synonymsThatAreCommon = set()
    for word in listSyn:
        if( word in app.freqWordDict ):
            synonymsThatAreCommon.add(word)
    maxRank = -1
    maxWord = ""
    if(len(synonymsThatAreCommon) > 0): #getting most common one
        for word in synonymsThatAreCommon:
            if( app.excludeSimilarLetters == True 
            or app.excludeSequenceLetters == True 
            or app.excludeMultipleDefinitions == True):
                if( (app.excludeSimilarLetters == True 
                and ( containsSimilarLetters(word) == False))
                    or ( app.exludedSequenceLetters == True 
                    and ( hasSameSequence(word, app) == False))
                    or (app.app.excludeMultipleDefinitions == True 
                    and ( hasMultipleDefinitions(word) == False))):
                    rank = app.freqWordDict[word]
                    if ( isVerb == True):
                        if (sentanceTenseClassifier.guess(word) 
                        == sentanceTenseClassifier.guess(origWord)):
                            if( maxRank == -1):
                                maxRank = rank
                                maxWord = word
                            elif( maxRank > rank):
                                maxRank = rank
                                maxWord = word
                    else:
                        if( maxRank == -1):
                                maxRank = rank
                                maxWord = word
                        elif( maxRank > rank):
                            maxRank = rank
                            maxWord = word
            else:
                rank = app.freqWordDict[word]
                if ( isVerb == True):
                    if (sentanceTenseClassifier.guess(word) 
                    == sentanceTenseClassifier.guess(origWord)):
                        if( maxRank == -1):
                            maxRank = rank
                            maxWord = word
                        elif( maxRank > rank):
                            maxRank = rank
                            maxWord = word
                else:
                    if( maxRank == -1):
                            maxRank = rank
                            maxWord = word
                    elif( maxRank > rank):
                        maxRank = rank
                        maxWord = word
    if maxWord == "":
        if isVerb == True:
            return listSyn[0]

        if(app.excludeSimilarLetters == True or app.excludeSequenceLetters 
        == True or app.excludeMultipleDefinitions == True):
            for i in range( 1, len(listSyn)):#index 0 is the orig word
                if( (app.excludeSimilarLetters == True 
                and ( containsSimilarLetters(word) == False))
                    or ( app.excludeSequenceLetters == True 
                    and ( hasSameSequence(word) == False))
                    or (app.excludeMultipleDefinitions == True 
                    and ( hasMultipleDefinitions(word) == False))):
                    return listSyn[i]
            return ""
        else:
            return listSyn[1] #index 0 is the orig word
    else:
        return maxWord
        
#takes the list of orig words and returns a list of the simplified words
def simplify(listOfOrigWords, app):
    # listOfOrigText = turnOrigTextIntoList(origText)
    newText = []
    for word in listOfOrigWords:
        if word in app.freqWordDict:
            newText = newText + [word]
        elif (sentanceTenseClassifier.isVerb(word) == True):
            listAlternativeVerbs = []
            for syn in wordnet.synsets(word): ###

                for lemm in syn.lemmas():###
                    sentanceWithReplacedSynonym = replaceWordInSentance(listOfOrigWords, word, lemm.name())
                    origSentance = makeSentance(listOfOrigWords)
                    if ( sentanceTenseClassifier.guess(lemm.name()) == sentanceTenseClassifier.guess(word)):
                        listAlternativeVerbs.append(lemm.name())###
            if( len(listAlternativeVerbs) > 1):
                simplestSyn = getSimplestSynonym(word, listAlternativeVerbs, 
                app, True)
                if( simplestSyn != ""):
                    newText = newText + [simplestSyn]
                else:
                    newText = newText + [word]
            else:
                newText = newText + [word]
        else:
            list_synonyms = []
            # help from https://www.datasciencelearner.com
            # /how-to-get-synonyms-and-antonyms-using-python-nltk/
            for syn in wordnet.synsets(word): ###
                for lemm in syn.lemmas():###
                    list_synonyms.append(lemm.name())###
            if( len(list_synonyms) > 1):
                simplestSyn = getSimplestSynonym(word, list_synonyms, app, False)
                if( simplestSyn != ""):
                    newText = newText + [simplestSyn]
                else:
                    newText = newText + [word]
            else:
                newText = newText + [word]
    return newText

sentanceTenseClassifier = SentanceTenseClassifier()
sentanceTenseClassifier.train("training_set.csv", "commonWordsThatArentVerbs.csv")
#training_set.csv and test_set.csv, sentances come from 
# https://englishgrammarsoft.com/examples-of-tenses-sentences-of-all-tenses/