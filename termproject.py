#################################################
# Term Project Simplifier
# name: Maelle Allanic
# andrew id: mallanic
#################################################
from cmu_112_graphics import *
from ButtonClass import *
from Simplify import *
from TextBoxClass import *

def simplifyButtonAction(app):
    origText = ""
    for i in range(0, app.numberOfLines-1):
        origText = origText + app.inputTextBox.getListOfLinesInTextBox()[i]
    #splits the string of words at the spaces into a list
    app.listOfOrigWords = []
    app.selectedWordIndex = 0
    lastIndexAdded = 0
    CurrBool = True
    for i in range(0, len(origText)):
        if isLetter(origText[i]) != CurrBool:
            app.listOfOrigWords.append(origText[lastIndexAdded:i])
            lastIndexAdded = i
            if( CurrBool == True):
                CurrBool = False
            else:
                CurrBool = True
    app.listOfOrigWords.append(origText[lastIndexAdded:len(origText)])
    #simplifies the origlist and gets the simplified list
    app.ListOfSimplifiedWords = simplify(app.listOfOrigWords, app)
    setUpResultandInfoBox(app)
    return None

def setUpResultandInfoBox(app):
    #adds the words from the list into the result string
    #makes the first word upercase(the selected word)

    app.resultTextBox.replaceTextInTextBoxWithTextFromListOfStringsWithUpperHighlight(app.ListOfSimplifiedWords, app.selectedWordIndex)

    #gets the definition of the selected word 
    # and puts it in the definition string
    # help from https://www.datasciencelearner.com
    #/how-to-get-synonyms-and-antonyms-using-python-nltk/
    #https://www.w3resource.com/python-exercises/nltk/nltk-corpus-exercise-6.php

    app.infoTextBox.clearTextInTextBox()
    selectedWord = app.ListOfSimplifiedWords[app.selectedWordIndex]

    string = selectedWord.upper()

    if ( app.wantDef == True):
        syn = wordnet.synsets(selectedWord) ###
        if( syn == []):
            string = string + ' No Definition'
            
        else:
            definition = syn[0].definition() ###
            string = string + ' ' + definition

    if ( app.wantSynonyms == True):
        list_synonyms = []
        for syn in wordnet.synsets(selectedWord): ###
            for lemm in syn.lemmas():###
                list_synonyms.append(lemm.name())###
        setOf3Synonyms = set()
        for i in range( 1 , len(list_synonyms)):
            if( len(setOf3Synonyms) <= 3):
                setOf3Synonyms.add(list_synonyms[i])
        if len(setOf3Synonyms) == 0:
            string = string + ' NO SYNONYMS'
        else:
            string = string + ' SYNONYMS:'
            for word in setOf3Synonyms:
                string = string + ' ' + word + ','
    
    if( app.wantSampleSentance == True):
        syn = wordnet.synsets(selectedWord) ###
        if( syn == []):
            string = string + ' NO SAMPLE SENTENCES'
        else:
            sampleSentances = syn[0].examples()
            if( len(sampleSentances) == 0 ):
                string = string + ' NO SAMPLE SENTENCES'
            else:
                string = string + ' SAMPLE SENTENCES:'
                for sentance in sampleSentances:
                    string = string + ' ' + sentance + "."

    app.infoTextBox.addChunkOfText(string)

def addKnownWordButtonAction(app):
    # We'll start you off with the code to read a file
    # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    # (The UTF-8 encoding helps work on all operating systems)
    with open(app.fileName, "r", encoding="utf-8") as f:
        fileString = f.read()
        with open(app.fileName, "a") as f:
            selectedWord = app.ListOfSimplifiedWords[app.selectedWordIndex]
            index = app.freqWordDictLastIndex + 1
            string = "\n" + str(index) + "," + selectedWord
            f.write(string)
    #reread the file and update the known words

def loginButtonAction(app):
    #only one line
    list = app.loginTextBox.getListOfLinesInTextBox()
    app.personName = list[0]
    #csv file wikipedia https://en.wiktionary.org
    # /wiki/Wiktionary:Frequency_lists/TV/2006/1-1000
    app.fileName = './' + app.personName + 'MostCommonWordsTV_2006_1-1000 - Sheet1.csv'
    try:
        app.freqWordDict = loadFreqWordsData(app.fileName, app)
        app.mode = 'settingsMode' 
    except:
        app.errorMessage = "NOT A VALID FILE, to create a new file, make a copy of commonWords in the folder and add your name at the front"
        




def clearButtonAction(app):
    #clears all the strings that are on the screen
    app.listOfOrigWords = []
    app.ListOfSimplifiedWords = []
    app.selectedWordIndex = 0
    app.inputTextBox.clearTextInTextBox()
    app.resultTextBox.clearTextInTextBox()
    app.infoTextBox.clearTextInTextBox()
    app.hoverRectangleInfo = None
    app.clickRectangleInfo = None
    
    
    return None

#switches between Screens
def switchButtonAction(app):
    if( app.mode == 'settingsMode'):
        app.mode = 'textBoxMode'
    else:
        app.mode = 'settingsMode' 

#Checkbox Actions
def similarLettersButtonAction(app):
    if( app.excludeSimilarLetters == False):
        app.excludeSimilarLetters = True
    else:
        app.excludeSimilarLetters = False

def sequenceLettersButtonAction(app):
    if( app.excludeSequenceLetters == False):
        app.excludeSequenceLetters = True
    else:
        app.excludeSequenceLetters = False
def multipleDefinitionsButtonAction(app):
    if (app.excludeMultipleDefinitions == False):
        app.excludeMultipleDefinitions = True
    else:
        app.excludeMultipleDefinitions = False

def wantDefButtonAction(app):
    if (app.wantDef == False):
        app.wantDef = True
    else:
        app.wantDef = False

def wantSynonymButtonAction(app):
    if( app.wantSynonyms == False):
        app.wantSynonyms = True
    else:
        app.wantSynonyms = False

def wantSampleSentancesButtonAction(app):
    if( app.wantSampleSentance == False):
        app.wantSampleSentance = True
    else:
        app.wantSampleSentance = False

###################################################################################
def loginMode_mousePressed(app, event):
    if(app.loginButton.CheckButtonClicked(event.x, event.y) == True):
        app.loginButton.buttonClicked(app)

#takes in app and event and deals with all the information 
def loginMode_keyPressed(app, event):

    if( event.key == "control-v"):
        app.loginTextBox.controlV()
        

    elif( event.key == "Space"):
        app.loginTextBox.space()
    elif( event.key == "Backspace"):
        app.loginTextBox.backspace()

    elif( len(event.key) > 1):
        #making sure no special keys appear
        return None
    else:
        app.loginTextBox.addRegLetter(event.key)

#draws text box and buttos for login mode
def loginMode_redrawAll(app, canvas):
    font = 'Consolas 12'
    #draws the 3 textboxes
    app.loginTextBox.drawTextBox(canvas)
    app.loginTextBox.drawWords(canvas)

    #draws the buttons
    app.loginButton.drawButton(canvas)
    canvas.create_text(25, 150, anchor = 'nw', text=app.errorMessage, 
    font="Arial 10", fill='black')

    canvas.create_text(25, 5, anchor = 'nw',
                        text="Enter your personalized file name begining:", 
                        font=font, fill="black")




#######################################################################################
    
def settingsMode_mousePressed(app, event):

    if( app.doneButton.CheckButtonClicked(event.x, event.y) == True):
        app.doneButton.buttonClicked(app)

    if( app.checkBoxSimilarLettersButton.CheckButtonClicked(event.x, event.y) 
    == True):
        app.checkBoxSimilarLettersButton.buttonClicked(app)
    
    if( app.checkBoxSequenceLettersButton.CheckButtonClicked(event.x, event.y) 
    == True):
        app.checkBoxSequenceLettersButton.buttonClicked(app)
    if( app.checkBoxMutlipleDefinitionsButton.CheckButtonClicked(event.x, 
    event.y) == True):
        app.checkBoxMutlipleDefinitionsButton.buttonClicked(app)

    if( app.checkBoxWantDefButton.CheckButtonClicked(event.x, event.y) == True):
        app.checkBoxWantDefButton.buttonClicked(app)
    
    if( app.checkBoxWantSynonymButton.CheckButtonClicked(event.x, event.y) 
    == True):
        app.checkBoxWantSynonymButton.buttonClicked(app)
    if( app.checkBoxWantSampleSentanceButton.CheckButtonClicked(event.x, 
    event.y) == True):
        app.checkBoxWantSampleSentanceButton.buttonClicked(app)

        
def settingsMode_redrawAll(app, canvas):
    canvas.create_text(100, 50, anchor = 'nw', text="Personalization", 
    font="Arial 15", fill='black')
    canvas.create_text(130, 150, anchor = 'nw', 
    text="Don't include words with mirrored letters (eg. bd, pq)", 
    font="Arial 10", fill='black')
    canvas.create_text(130, 250, anchor = 'nw', 
    text="Don't include words with same the sequence letters (eg. although vs thought)", 
        font="Arial 10", fill='black')
    canvas.create_text(130, 350, anchor = 'nw', 
    text="Don't include words with multiple meanings (eg. siren)", 
    font="Arial 10", fill='black')
    app.doneButton.drawButton(canvas)
    app.checkBoxSimilarLettersButton.drawButton(canvas)
    app.checkBoxSequenceLettersButton.drawButton(canvas)
    app.checkBoxMutlipleDefinitionsButton.drawButton(canvas)

    canvas.create_text(750, 50, anchor = 'nw', text="Description", 
    font="Arial 15", fill='black')
    canvas.create_text(780, 150, anchor = 'nw', text="Include Definitions", 
    font="Arial 10", fill='black')
    canvas.create_text(780, 250, anchor = 'nw', text="Include Synonyms", 
    font="Arial 10", fill='black')
    canvas.create_text(780, 350, anchor = 'nw', text="Include Sample Sentences", 
    font="Arial 10", fill='black')
    app.checkBoxWantDefButton.drawButton(canvas)
    app.checkBoxWantSynonymButton.drawButton(canvas)
    app.checkBoxWantSampleSentanceButton.drawButton(canvas)
######################################################################################

    
#takes in app and event and deals with all the information 
def textBoxMode_keyPressed(app, event):

    if( event.key == "control-v"):
        app.inputTextBox.controlV()
        

    elif( event.key == "Space"):
        app.inputTextBox.space()
    elif( event.key == "Backspace"):
        app.inputTextBox.backspace()

    elif( len(event.key) > 1):
        #making sure no special keys appear
        return None
    else:
        app.inputTextBox.addRegLetter(event.key)


def textBoxMode_mousePressed(app, event):
    #checks if the buttons are pressed and does the action
    if( app.simplifyButton.CheckButtonClicked(event.x, event.y) == True):
        app.simplifyButton.buttonClicked(app)
    
    if( app.clearButton.CheckButtonClicked(event.x, event.y) == True):
        app.clearButton.buttonClicked(app)
    if( app.personalizeButton.CheckButtonClicked(event.x, event.y) == True):
        app.personalizeButton.buttonClicked(app)

    if( len(app.ListOfSimplifiedWords) != 0):
        if ( app.ListOfSimplifiedWords[app.selectedWordIndex]  
        not in app.freqWordDict):
            if (app.addKnownWordButton.CheckButtonClicked(event.x, event.y) 
            == True):
                app.addKnownWordButton.buttonClicked(app)
    word = hoverBox(app, event, 'click')
    if (word != None):
        for i in range(0, len(app.ListOfSimplifiedWords)):
            if( app.ListOfSimplifiedWords[i] == word):
                app.selectedWordIndex = i
        setUpResultandInfoBox(app)

def textBoxMode_mouseMoved(app, event):
    hoverBox(app, event, 'hover')

#creates the box around the word that the user is hovering.
def hoverBox(app, event, clickOrHover):
    25, 425, 700, 775
    topX, topY, bottomX, bottomY = app.resultTextBox.getDim()
    numberOfLines = app.resultTextBox.getNumberOfLines()
    listOfLinesInTextBox = app.resultTextBox.getListOfLinesInTextBox()
    if( topX<= event.x <= bottomX and topY <= event.y <= bottomY):
        
        margin = 5
        y = event.y - topY - margin
        x = event.x - topX - margin
        beforeBoxX = topX + margin
        beforeBoxY = topY + margin
        if 0 < y <= 20*numberOfLines:
            lineOn = y//20
            letterOn = x//9
            if( len(listOfLinesInTextBox[lineOn]) >= letterOn and letterOn >=0 
            and len(listOfLinesInTextBox[lineOn]) > 0):
                if( isLetter(listOfLinesInTextBox[lineOn][letterOn:letterOn+1]) 
                == True):
                    firstLetterInWordIndex = 0
                    lastLetterInWordIndex = 0

                    for i in range(0, len(listOfLinesInTextBox[lineOn])):
                        if ( i < letterOn):
                            if( isLetter(listOfLinesInTextBox[lineOn][i:i+1]) 
                            == False and 
                            isLetter(listOfLinesInTextBox[lineOn][i+1:i+2]) 
                            == True):
                                firstLetterInWordIndex = i+1
                        if ( i >= letterOn):
                            if(lastLetterInWordIndex == 0 and 
                            isLetter(listOfLinesInTextBox[lineOn][i:i+1]) 
                            == True 
                            and isLetter(listOfLinesInTextBox[lineOn][i+1:i+2]) 
                            == False):
                                lastLetterInWordIndex = i
                        
                    if lastLetterInWordIndex < firstLetterInWordIndex:
                        return
                    if( clickOrHover == 'click'):
                        app.clickRectangleInfo = firstLetterInWordIndex*9+beforeBoxX, 20*lineOn+beforeBoxY, (lastLetterInWordIndex+1)*9+beforeBoxX, 20*(lineOn+1)+beforeBoxY, "yellow"
                        return listOfLinesInTextBox[lineOn][firstLetterInWordIndex:lastLetterInWordIndex+1]
                    if( clickOrHover == 'hover'):
                        app.hoverRectangleInfo = firstLetterInWordIndex*9+beforeBoxX, 20*lineOn+beforeBoxY, (lastLetterInWordIndex+1)*9+beforeBoxX, 20*(lineOn+1)+beforeBoxY, "gray"
                        return
        app.hoverRectangleInfo = None
        
#checks if the char is a letter in the alphabet
def isLetter(char):
    char = char.lower()
    string = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(0, len(string)):
        if ( string[i:i+1] == char):
            return True
    
    return False



def textBoxMode_redrawAll(app, canvas):
    font = 'Consolas 12'
    #draws the 3 textboxes
    app.inputTextBox.drawTextBox(canvas)
    app.inputTextBox.drawWords(canvas)
    app.resultTextBox.drawTextBox(canvas)
    if( app.hoverRectangleInfo != None):
        topX, topY, bottomX, bottomY, color = app.hoverRectangleInfo
        canvas.create_rectangle(topX, topY, bottomX, 
        bottomY, fill=color, width=0)
    if( app.clickRectangleInfo != None):
        topX, topY, bottomX, bottomY, color = app.clickRectangleInfo
        canvas.create_rectangle(topX, topY, bottomX, 
        bottomY, fill=color, width=0)
    app.resultTextBox.drawWords(canvas)
    app.infoTextBox.drawTextBox(canvas)
    app.infoTextBox.drawWords(canvas)


    app.simplifyButton.drawButton(canvas)
    app.clearButton.drawButton(canvas)
    app.personalizeButton.drawButton(canvas)

    

    if( len(app.ListOfSimplifiedWords) != 0):
        if ( app.ListOfSimplifiedWords[app.selectedWordIndex]  
        not in app.freqWordDict):
            app.addKnownWordButton.drawButton(canvas)


    canvas.create_text(25, 5, anchor = 'nw',
                        text="Enter Original Message:", 
                        font=font, fill="black")

    canvas.create_text(25, 405, anchor = 'nw',
                        text="Personalized Simplification:", 
                        font=font, fill="black")
    canvas.create_text(750, 405, anchor = 'nw',
                        text="Description:", 
                        font=font, fill="black")



######################################################################
def appStarted(app):
    app.mode = 'loginMode'
    ######################
    #loginMode
    app.personName = ""
    app.fileName = ""
    app.errorMessage = ""
    app.freqWordDict = dict()
    app.freqWordDictLastIndex = 0
    app.loginTextBox = TextBox(25, 25, 210, 60,'light gray', 
    'gray', 2, 'Consolas 12', 'black', 1, 20, True)
    app.loginButton = Button(80, 80, 155, 105, "UseThisFile", 'light gray', 
    'gray', 2, "Arial 10", 'black', loginButtonAction)
    



    ####################
    #settings mode
    app.excludeSimilarLetters = False
    app.excludeSequenceLetters = False
    app.excludeMultipleDefinitions = False
    app.wantDef = False
    app.wantSynonyms = False
    app.wantSampleSentance = False

    app.doneButton = Button(1300, 25, 1375, 55, "Done", 'light gray', 'gray', 2, 
    "Arial 10", 'black', switchButtonAction)
    app.checkBoxSimilarLettersButton = ToggleButton(100, 150, 120, 170, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', similarLettersButtonAction)
    app.checkBoxSequenceLettersButton = ToggleButton(100, 250, 120, 270, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', sequenceLettersButtonAction)
    app.checkBoxMutlipleDefinitionsButton = ToggleButton(100, 350, 120, 370, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', multipleDefinitionsButtonAction)

    app.checkBoxWantDefButton = ToggleButton(750, 150, 770, 170, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', wantDefButtonAction)
    app.checkBoxWantSynonymButton = ToggleButton(750, 250, 770, 270, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', wantSynonymButtonAction)
    app.checkBoxWantSampleSentanceButton = ToggleButton(750, 350, 770, 370, "", 
    'light gray', 'white',
    'gray', 2, "Arial 10", 'black', wantSampleSentancesButtonAction)

    ##################
    #textbox mode

    app.numberOfLines = 5
    app.numberOfLettersInALine = 75
    app.listOfOrigWords = []
    app.ListOfSimplifiedWords = []
    app.selectedWordIndex = 0
    app.hoverRectangleInfo = None
    app.clickRectangleInfo = None

    app.inputTextBox = TextBox(25, 25, 700, 375,'light gray', 
    'gray', 2, 'Consolas 12', 'black', app.numberOfLines, 
    app.numberOfLettersInALine, True)
    app.resultTextBox = TextBox(25, 425, 700, 775,'light gray', 
    'gray', 2, 'Consolas 12', 'black', app.numberOfLines, 
    app.numberOfLettersInALine, False)
    app.infoTextBox = TextBox(750, 425, 1375, 775,'light gray', 
    'gray', 2, 'Consolas 12', 'black', app.numberOfLines, 70, False)
    #creates the buttons
    app.simplifyButton = Button(300, 385, 375, 415, "Simplify", 'light gray', 
    'gray', 2, "Arial 12", 'black', simplifyButtonAction)
    app.clearButton = Button(400, 385, 475, 415, "Clear", 'light gray', 
    'gray', 2, "Arial 12", 'black', clearButtonAction)
    app.personalizeButton = Button(1300, 25, 1375, 55, "Personalize", 
    'light gray', 'gray', 2, "Arial 10", 'black', switchButtonAction)

    app.addKnownWordButton = Button(1230, 325, 1375, 355, 
    "Add to known words file", 'light gray', 'gray', 2, "Arial 10", 
    'black', addKnownWordButtonAction)



runApp(width=1400, height=800)