import random
from collections import Counter

def readAnswers(answers):
    with open("answers.txt") as file:
        lines = file.readlines()
        for line in lines:
            answers.append(line.strip())

def filterAnswers(answers,g,y,b):
    answers = filterG(answers,g)
    answers = filterY(answers,y)
    answers = filterB(answers,b)
    # print(answers)
    return answers


def filterG(answers, g):
    for pair in g:
        letter = pair[0]
        index = pair[1]
        answers = list(filter(lambda word: word[index] == letter, answers))
    return answers

def filterY(answers, y):
    for pair in y:
        letter = pair[0]
        index = pair[1]
        answers = list(filter(lambda word: letter in word and word[index] != letter, answers))

    return answers

def filterB(answers, b):
    for pair in b:
        letter = pair[0]
        index = pair[1]
        answers = list(filter(lambda word: letter not in word, answers))

    return answers

def filterSpecial(answers, letter, gCount, yCount, bCount, gIndexes, yIndexes, bIndexes):
    global specialLetter
    specialLetter = letter
    if(gCount + yCount == 0):
        
        answers = filterB(answers,[letter,bIndexes[0]])
    else:
        g = []
        y = []
        for i in range(gCount):
            g.append([letter,gIndexes[i]])
        for i in range(yCount):
            y.append([letter,yIndexes[i]])
        answers = filterG(answers,g)
        answers = filterY(answers,y)
        answers = list(filter(filterSpecialHelper,answers))


        # TO DO 
        # if bCount >=1 , then we know the max
    # print("special",answers)
    return answers

def filterSpecialHelper(word):
    count = Counter(word)
    m = gCount + yCount
    # print(bCount,word)
    if(bCount >= 1):
        if(count[specialLetter] == m):
            return True
        else:
            return False
    else:
        # bcount is 0, so check count for at least
        if(count[specialLetter] >= m):
            return True
        else:
            return False


def suggest(answers):
    if not answers:
        print("No possible answers! Maybe you made a typo?")
        return
    if(len(answers) == 1):
        print("The winning word is {}!".format(answers[0]))
        return 1
    scores = []
    for word in answers:
        # Give each word a score
        score = 0
        for letter in word:
            if(letter == 'a' or letter == 'e'):
                score += 1
            elif(letter == 's'):
                score += .95
            elif(letter == 'o' or letter == 'r' or letter == 'i'):
                score += .9
            elif(letter == 'l' or letter == 'n' or letter == 't'):
                score += .85
            elif (letter == 'u'):
                score += .82
            elif (letter =='d' or letter =='c' or letter =='y' or letter =='m' or letter =='p' or letter =='h' or letter =='b' or letter =='g' or letter =='k'):
                score += .75
            elif(letter == 'f' or letter =='v' or letter =='w'):
                score += .65
            elif(letter == 'z' or letter =='j' or letter =='x'):
                score += .5
            elif(letter == 'q'):
                score += .4
        # add score if every letter is unique 1
        score -= len(word) - len(set(word))
        scores.append([word,score])
        scores.sort(key=lambda x: x[1],reverse=True)
    # print(scores)
    maxScore = scores[0][1]
    bestWords = list(filter(lambda pair: pair[1] == maxScore,scores))
    print("There are only {} reamining possible words!".format(len(answers)))
    print("We suggest you use the word: {}".format(random.choice(bestWords)[0]))
    print()
            

if __name__ == "__main__":
    global bCount
    global yCount
    global gCount
    global specialLetter
    bCount = 0
    gCount = 0
    yCount = 0
    specialLetter = ''
    answers = []
    solved = False
    readAnswers(answers)
    print()
    print("Please type in your first guess with the format WORD:STATUS")
    print("Please use the letter G for green, Y for yellow, and B for black")
    print("For example, if I start with TRACE and T is green and A is yellow, this would be the input")
    print("TRACE:GBYBB")
    print()
    while(not solved):
        g = []
        y = []
        b = []
        special = []
        print("Please type in your answer and status in the form WORD:STATUS")
        a = input()
        if(a == 'win'):
            print("Congrats!")
            break
        # regex? 
        # FILTER ANSWERS
        a = a.split(":")
        word = a[0].lower()
        status = a[1].lower()
        count = Counter(word)
        for i in range(len(word)):
            letter = word[i]
            # CHECK IF LETTER APPEARS MULTIPLE TIMES IN WORD
            
            if(count[letter] > 1):
                if(letter in special):
                    pass
                special.append(letter)
                arr = []
                gCount = 0
                yCount = 0
                bCount = 0
                gIndexes = []
                yIndexes = []
                bIndexes = []
                for j in range(len(word)):
                    if(word[j] == letter):
                        if(status[j] == 'g'):
                            gCount += 1
                            gIndexes.append(j)
                        elif(status[j] == 'y'):
                            yCount += 1
                            yIndexes.append(j)
                        elif(status[j] == 'b'):
                            bCount += 1
                            bIndexes.append(j)
                answers = filterSpecial(answers, letter, gCount, yCount, bCount, gIndexes, yIndexes, bIndexes)
            else:
                letterStatus = status[i]
                if(letterStatus == 'g'):
                    g.append([letter,i])
                elif(letterStatus == 'y'):
                    y.append([letter,i])
                elif(letterStatus == 'b'):
                    b.append([letter,i])
        special.clear()
        answers = filterAnswers(answers,g,y,b)
        i = suggest(answers)
        if(i == 1):
            break
