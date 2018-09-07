from random import randint,random
from termcolor import colored
import time
import requests


def getword():
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

    response = requests.get(word_site)
    WORDS = response.content.splitlines()

    word = (WORDS[randint(0,len(WORDS)-1)])
    word = str(word)
    return(word[2:-1].lower())


def display(userWord,oldGuesses,guesses,maxGuesses):
    printer = ""
    for x in userWord:
        printer+=x
        printer+=" "
    print(printer)
    printer = "Corruption:["
    printer+=colored("██","red")*round(guesses/(maxGuesses)*10)
    printer+=colored("██","white")*round((maxGuesses-guesses)/(maxGuesses)*10)
    printer+="]"
    print(printer)
    printer = "Tried letters: "
    for x in oldGuesses:
        if(len(x)==1):
            printer+=x+", "
    print (printer)

def userGuess(oldGuesses):
    allowedGuesses = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    while(True):
        print("type a letter to guess 1\ntype a string to guess the word")
        guess = (input()).upper()
        if(guess in oldGuesses):
            print(colored("ERROR: INPUT ALREADY TESTED","grey","on_red",attrs=["blink"]))
        elif(guess in allowedGuesses):
            return(guess,"C")
        elif(len(guess)>1):
            valid = True
            for x in list(guess):
                if(x not in allowedGuesses):
                    valid = False
            if(valid):
                print("are you sure you would like to guess {}?".format(colored(guess,"blue")))
                test = input("(y/n): ")
                if((test).upper()=="Y"):
                    return(guess,"S")
            else:
                print(colored("ERROR: INPUT NOT VALID","grey","on_red",attrs=["blink"]))
        else:
            print(colored("ERROR: INPUT NOT VALID","grey","on_red",attrs=["blink"]))


def testIn(guess,word,userWord):
    guess = guess.lower()

    while(guess in word):
        wordpos = word.index(guess)
        word = changeL(word,"_",wordpos)
        # userWord = colored(userWord,"white")
        userWord = changeL(userWord,guess,wordpos)
        if(guess not in word):
            return(word,userWord,False)
    else:
        return(word,userWord,True)

def changeL(str,newChar,index):
    str = list(str)
    str[index] = newChar
    rStr = ""
    for x in str:
        rStr+=x
    return rStr


def run():
    word = getword()
    originWord = word
    userWord = "_"*len(word)
    guesses = 0
    maxGuesses = 7
    oldGuesses = []
    guessU = ""
    while(True):
        display(userWord,oldGuesses,guesses,maxGuesses)
        guessU,guessType = userGuess(oldGuesses)
        oldGuesses.append(guessU)
        print(colored("RECEIVED...","grey","on_blue",attrs=["blink","underline"]))
        print(colored("PROCESSING...","grey","on_blue",attrs=["blink","underline"]))
        time.sleep(random()*2)
        if(guessType == "C"):
            word,userWord,failed = testIn(guessU,word,userWord)
            if(failed):
                guesses+=1
                print(colored("ERROR: GUESS NOT IN WORD","grey","on_red",attrs=["blink"]))
                print(colored("WARNING: CORRUPTION LEVEL RISING","grey","on_red",attrs=["blink"]))
            else:
                print(colored("SUCCESS","grey","on_green"))
        else:
            if(guessU.lower() == originWord):
                print(colored("SUCCESS","grey","on_green"))
                userWord=originWord
            else:
                guesses+=1
                print(colored("ERROR: WORD GUESS INCORECT","grey","on_red",attrs=["blink"]))
                print(colored("WARNING: CORRUPTION LEVEL RISING","grey","on_red",attrs=["blink"]))
        if(userWord==originWord):
            print(originWord)
            return("Victory")
        elif(guesses>=maxGuesses):
            print(originWord)
            return("Failure")


def Failure():
    print("u suk")





def Victory():
    print("u good")




result = run()
if(result == "Victory"):
    Victory()
else:
    Failure()
