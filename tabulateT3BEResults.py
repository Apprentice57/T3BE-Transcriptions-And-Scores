import sys, os

files = []

folder = "answers"

#add all txt files in /answers as the source of question data.
for filename in os.listdir("./" + folder):
    if filename.endswith(".txt") and filename != "nextquestion.txt":
        files.append(filename)

files.sort()

mostRecentWindow = int(sys.argv[1])

listThomasFirst = True

def readFile(filePath):
    results = []

    try:
        with open(filePath, 'r') as file:
            for line in file:
                line = line.strip()

                if line:
                    words = line.split()
                    if len(words) < 2:
                        raise Exception("Malformed input file " + filePath + ". All lines should have 2 or more words.")

                    results.append((words[0], words[1]))

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return results

#Taking in the key,value pairs from a file, add the meta info within to a dictionary
def makeInnerMetaDict(rawData, file):
    #looping through the whole thing each time is slow, but who cares
    hasQNumber = False
    hasQType = False
    hasBonus = False
    hasCounts = False
    hasRepeat = False
    hasAnswer = False

    metadataDict = {}
    #metadataDict["filename"] = f

    for d in rawData:
        key, value = d
        match key:
            case "Question":
                hasQNumber = True
                if (value.isdigit()):
                    metadataDict["Question"] = value
                else:
                    raise Exception("Sorry, File " + file + " has a malformed Number metadata entry. It must be an integer.")
            case "QuestionType":
                hasQType = True
                if (value == "Public" or value == "Patron" or value == "ThomasOnly"):
                    metadataDict["QuestionType"] = value
                else:
                    raise Exception("Sorry, File " + file + " has a malformed QuestionType metadata entry. It must be 'Public', 'Patron', or 'ThomasOnly'")
            case "IsBonus":
                hasBonus = True
                if (value == "Yes" or value == "No"):
                    metadataDict["IsBonus"] = value
                else:
                    raise Exception("Sorry, File " + file + " has a malformed IsBonus metadata entry. It must be 'Yes' or 'No'")
            case "CountsForThomas":
                hasCounts = True
                if (value == "Yes" or value == "No"):
                    metadataDict["CountsForThomas"] = value
                else:
                    raise Exception("Sorry, File " + file + " has a malformed CountsForThomas metadata entry. It must be 'Yes' or 'No'")
            case "IsRepeat":
                hasRepeat = True
                if (value == "Yes" or value == "No"):
                    metadataDict["IsRepeat"] = value
                else:
                    raise Exception("Sorry, File " + file + " has a malformed IsRepeat metadata entry. It must be 'Yes' or 'No'")
            case "Answer":
                hasAnswer = True
                answer = value[0].upper()
                if (answer == "A" or answer == "B" or answer == "C" or answer == "D"):
                    metadataDict["Answer"] = answer
                else:
                    raise Exception("Sorry, File " + file + " has a malformed Answer entry. It must begin with 'A','B','C', or 'D', case insensitive.")

    hasAllMetadata = hasQNumber and hasQType and hasBonus and hasCounts and hasRepeat and hasAnswer

    if(not(hasAllMetadata)):
        raise Exception("Sorry, File " + file + " is missing Metadata. You must include all these fields: 'Question', 'QuestionType', 'IsBonus', 'CountsForThomas', 'IsRepeat', and 'Answer'.")

    if (metadataDict["IsBonus"] == "Yes"):
        metadataDict["Question"] = "b" + metadataDict["Question"]

    return metadataDict

def makeInnerAnswerDict(rawData, file):
    hasAnswers = False
    answerDict = {}

    for d in rawData:
        key, value = d
        if ((key != "Question") and (key != "QuestionType") and (key != "IsBonus") and (key != "CountsForThomas") and (key != "IsRepeat") and (key != "Answer")):
            answerDict[key] = value

    if (answerDict == {}):
        raise Exception("Sorry, File " + file + "Does not have any validly formatted answers. There must be at least one.")

    return answerDict

#def fileNameToQuestionName

def compileNames(fullAnswers):
    names = []
    for a in fullAnswers:
        oneAnswerSet = fullAnswers[a]
        for o in oneAnswerSet:
            names.append(o)


    #convert to set to remove duplicates, then back to a list and sort it
    names = sorted(list(set(names)), key=str.lower)

    if listThomasFirst:
        names.remove("NegatronThomas")
        names.insert(0, "NegatronThomas")

    underscores = "____-__________-____"
    if underscores in names:
        names.remove(underscores)
        names.append(underscores)

    return names

def fillNonAnswers(fullAnswers, names):
    for a in fullAnswers:
        oneAnswerSet = fullAnswers[a]

        for n in names:
            if not (n in oneAnswerSet):
                oneAnswerSet[n] = "X"
    return

#cutoff will be a number like 5, 10, to show how someone did on the most recent x questions
def calculateStats(fullAnswers, fullMD, names, cutoff):
    totalQuestions = len(files)
    numToSkip = totalQuestions - cutoff

    namesWithStats = {}

    for n in names:
        numCorrect = 0
        numCorrectSub = 0

        numAnswered = 0
        numAnsweredSub = 0

        i = 1
        for m in fullMD:
            #do not count question if bonus
            if fullMD[m]["IsBonus"] == "No":
                correctAnswer = fullMD[m]["Answer"]
                userAnswer = fullAnswers[m][n]

                #haven't skipped enough, only count for overall stats
                if i < numToSkip:
                    if userAnswer != "X":
                        numAnswered += 1

                        if userAnswer == correctAnswer:
                            numCorrect += 1

                    if n == "NegatronThomas":
                        #For Thomas, no change if it's a repeat he got wrong
                        #But don't count the question if it's a repeat he got right
                        if fullMD[m]["IsRepeat"] == "Yes":
                            if userAnswer == correctAnswer:
                                numAnswered -= 1
                                numCorrect -= 1
                                #i -= 1

                #count for both stats
                else:
                    if userAnswer != "X":
                        numAnswered += 1
                        numAnsweredSub += 1

                        if userAnswer == correctAnswer:
                            numCorrect += 1
                            numCorrectSub += 1

                    if n == "NegatronThomas":
                        #For Thomas, no change if it's a repeat he got wrong
                        #But don't count the question if it's a repeat he got right
                        if fullMD[m]["IsRepeat"] == "Yes":
                            if userAnswer == correctAnswer:
                                numAnswered -= 1
                                numAnsweredSub -= 1
                                numCorrect -= 1
                                numCorrectSub -= 1
                                #i -= 1
                i += 1

        shortRecord = str(numCorrectSub) + "/" + str(numAnsweredSub)
        if (numAnsweredSub != 0):
            shortRecordPerc = float(numCorrectSub) / float(numAnsweredSub)
        else:
            shortRecordPerc = "0.0"

        record = str(numCorrect) + "/" + str(numAnswered)
        recordPerc = float(numCorrect) / float(numAnswered)

        userStats = {"shortRecord":shortRecord, "shortRecordPerc":shortRecordPerc, "record":record, "recordPerc":recordPerc, \
                "shortNumCorrect":numCorrectSub, "shortNumAnswered":numAnsweredSub, "numCorrect":numCorrect, "numAnswered":numAnswered}

        namesWithStats[n] = userStats

    return namesWithStats

#This is much simpler due to the datatypes already being organized by question. The result is
#appended to fullMD instead of being returned
def calculateStatsQuestion(fullAnswers, fullMD, names):
    for m in fullMD:
        numCorrect = 0
        numAnswered = 0
        correctAnswer = fullMD[m]["Answer"]
        for n in names:
            userAnswer = fullAnswers[m][n]
            if userAnswer != "X":
                numAnswered += 1
                if userAnswer == correctAnswer:
                    numCorrect += 1

        record = str(numCorrect) + "/" + str(numAnswered)
        fullMD[m]["Record"] = record
    return

def makeFiveWide(q):
    match len(q):
        case 1:
            return("  " + q + "  ")
        case 2:
            return("  " + q + " ")
        case 3:
            return(" " + q + " ")
        case 4:
            return(" " + q)
        case 5:
            return(q)
        case _:
            return("-----")

def makeThreeWide(q):
    match len(q):
        case 1:
            return(" " + q + " ")
        case 2:
            return( q + " ")
        case 3:
            return(q)
        case _:
            return("---")

def findLongestUsername(names):
    maxLength = 0
    for s in names:
        maxLength = max(maxLength, len(s))

    return maxLength

def spacerLengths(longerWord, shorterWord):
    difference = longerWord - shorterWord

    if difference < 0:
        raise Exception("You sent a word that is too long to space into the 'longer' word.")

    spaces = difference + 3

    lenBefore = int(spaces / 2)
    lenAfter = spaces - int(spaces / 2) - 1

    return lenBefore, lenAfter

def spacesShortRecord(cutoff):
    if len(str(cutoff)) == 1:
        beforeSpaces = 2
        afterSpaces = 2
    elif len(str(cutoff)) == 2:
        beforeSpaces = 1
        afterSpaces = 2
    elif len(str(cutoff)) == 3:
        beforeSpaces = 1
        afterSpaces = 1
    else:
        beforeSpaces = 1
        afterSpaces = 1

    return beforeSpaces, afterSpaces

def printFirstCell(word, longestName):
    lenBefore, lenAfter = spacerLengths(longestName, len(word))

    print("|" + (" " * lenBefore) + word + (" " * lenAfter) + "|", end = "")
    return

def calculateTotalLastX(questionsToIterate, stats):
    print(stats)
    return 10 * "-"

def calculateTotalTotal():
    return 10 * "-"


def printTable(fullAnswers, fullMD, names, stats, cutoff):
    questionsToIterate = files[-1 * cutoff:]
    legend = "Username / Q#->"

    longestName = findLongestUsername(names)
    if (len(legend) > longestName):
        longestName = len(legend)

    lineWidth = 26 + 6 * len(questionsToIterate) + longestName

    divider = " " + ("_" * (lineWidth - 2)) + " "
    interstitial = (divider.replace("_", "-")).replace(" ", "|")

    lenBefore, lenAfter = spacerLengths(longestName, len("username"))

    #----printing begins ----#
    #print header
    print(divider)
    printFirstCell(legend, longestName)
    for m in questionsToIterate:
        print(makeFiveWide(fullMD[m]["Question"]), end = "|")
    beforeSpaces, afterSpaces = spacesShortRecord(cutoff)
    shortRecordString = (" " * beforeSpaces) + "Last " + str(cutoff) + (" " * afterSpaces)
    recordString = "  Total   "
    print(shortRecordString + "|" +  recordString + "|")

    print(interstitial)

    #print correct answers first
    printFirstCell("Correct Answer", longestName)
    for m in questionsToIterate:
        print(makeFiveWide(fullMD[m]["Answer"]), end = "|")
    print((" " * len(shortRecordString)) + "|" + (" " * len(recordString)) + "|")

    print(interstitial)

    #print each user's answers and stats
    totalCorrectShort = 0
    totalAnsweredShort = 0
    totalCorrect = 0
    totalAnswered = 0
    for n in names:
        if stats[n]["shortRecord"] == "0/0":
            continue

        printFirstCell(n, longestName)
        for m in questionsToIterate:
            answer = fullAnswers[m][n]
            if answer == "X":
                answer = " "
            print(makeFiveWide(answer), end = "|")
        shortRecord = stats[n]["shortRecord"]
        record = stats[n]["record"]

        totalCorrectShort += stats[n]["shortNumCorrect"]
        totalAnsweredShort += stats[n]["shortNumAnswered"]
        totalCorrect += stats[n]["numCorrect"]
        totalAnswered += stats[n]["numAnswered"]

        beforeSpaces = int((len(shortRecordString) - len(shortRecord))/2)
        afterSpaces = (len(shortRecordString) - len(shortRecord)) - beforeSpaces
        print((beforeSpaces * " ") + shortRecord + (afterSpaces * " "), end = "|")
        beforeSpaces = int((len(recordString) - len(record))/2)
        afterSpaces = (len(recordString) - len(record)) - beforeSpaces
        print((beforeSpaces * " ") + record + (afterSpaces * " ") + "|")

    print(interstitial)

    printFirstCell("Total:", longestName)
    for m in questionsToIterate:
        print(makeFiveWide(fullMD[m]["Record"]), end = "|")

    lastXStat = str(totalCorrectShort) + "/" + str(totalAnsweredShort)
    totalStat = str(totalCorrect) + "/" + str(totalAnswered)

    beforeSpaces = int((len(shortRecordString) - len(lastXStat))/2)
    afterSpaces = (len(shortRecordString) - len(lastXStat)) - beforeSpaces
    print((beforeSpaces * " ") + lastXStat + (afterSpaces * " "), end = "|")

    beforeSpaces = int((len(recordString) - len(totalStat))/2)
    afterSpaces = (len(recordString) - len(totalStat)) - beforeSpaces
    print((beforeSpaces * " ") + totalStat + (afterSpaces * " ") + "|")

    print(interstitial)
    print("")

    return

fullMD = {}
fullAnswers = {}
for f in files:
    filePath = "./" + folder + "/" + f
    results = readFile(filePath)
    fullMD[f] = makeInnerMetaDict(results, f)
    fullAnswers[f] = makeInnerAnswerDict(results, f)

#make list of all users who answered at least one question
participants = compileNames(fullAnswers)

#For convenience, add "X" as the answer for any question not answered by a user
fillNonAnswers(fullAnswers, participants)

#calculate stats per user and per question
stats = calculateStats(fullAnswers, fullMD, participants, mostRecentWindow)
calculateStatsQuestion(fullAnswers, fullMD, participants)

printTable(fullAnswers, fullMD, participants, stats, mostRecentWindow)

