import re
import sys
import os


def checkComments(myString, startIndex):
    regular_result = re.search(r'({).*?(})', myString[startIndex:])
    if (regular_result is None):
        # No Closing bracket found
        # Here we raise an checkError
        return None
    else:  # index of {
        return regular_result.end(0) + startIndex  # index of }


def checkDigits(myString, start_index):
    regular_result = re.search(r'([0-9]+) *?', myString[start_index:])

    if (regular_result is None):

        # No digits found

        return None

    else:

        return regular_result.end(0) + start_index  # index of ending digit


def inAssign(myString, startIndex):
    regular_result = re.search(r'([:=])', myString[startIndex:])
    if(regular_result is None):
        return None
    else:
        return regular_result.end(0) + startIndex


def isLetters(string, startIndex):
    ss = re.search("[a-zA-Z0-9]+", string[startIndex:])
    if(ss):
        return ss.end(0) + startIndex
    else:
        return None


def checkError(endIndex):

    if endIndex is None:

        print("Error")

        sys.exit()

    else:

        return


def writeData(filename, data):

    with open(filename, 'w') as f:
        for tuple in data:
            line = str(tuple[0]) + ' ' + str(tuple[1])

            f.write(line + "\n")


def readData(filename):

    with open(filename, 'r') as f:
        return f.read()


# print("Enter Tiny Language Input")
# fileName = input()
# inputCode = readData(fileName)
# print(inputCode)
# inputCode = sys.stdin.read()   # Use Ctrl d to stop the input
# lines = []
# while True:
#     line = input()
#     if line:
#         lines.append(line)
#     else:
#         break
# inputCode = '\n'.join(lines)
# print(lines)
# print(inputCode)

def Scan(inputCode):
    specialChars = ['(', ')', '+', '-', '*', '/',
                    '=', ';', '<', '>', '<=', '>=']
    specialCharsTuple = [('(', "OPENBRACKET"), (')', "CLOSEDBRACKET"), ('+', "PLUS"), ('-', "MINUS"), ('*', "MULT"), ('/', "DIV"),
                         ('=', "EQUAL"), (';', "SEMICOLON"), ('<', "LESSTHAN"), ('>', "GREATERTHAN"), ('<=', "LESSTHANOREQUAL"), ('<=', "GREATERTHANOREQUAL")]
    specialCharsType = ["OPENBRACKET", "CLOSEDBRACKET", "PLUS", "MINUS", "MULT", "DIV",
                         "EQUAL", "SEMICOLON", "LESSTHAN","GREATERTHAN", "LESSTHANOREQUAL", "GREATERTHANOREQUAL"]

    reservedWords = ["if", "then", "else", "end",
                     "repeat", "until", "read", "write"]
                     
    reservedWordsTuple = [("if", "IF"), ("then", "THEN"), ("else", "ELSE"), ("end", "END"), (
        "repeat", "REPEAT"), ("until", "UNTIL"), ("read", "READ"), ("write", "WRITE")]
    reservedWordsType = [ "IF",  "THEN",  "ELSE", "END", 
         "REPEAT",  "UNTIL",  "READ",  "WRITE"]
    previousState = "start"
    currentState = "start"
    startIndex = 0
    endIndex = 0
    tokens = []
    i = 0
    while i < len(inputCode):
        if currentState == 'start':
            if inputCode[i] == ' ' or inputCode[i] == '\n':
                i = i + 1
                currentState == "start"
            elif inputCode[i] == '{':
                previousState = "start"
                currentState = "inComment"
                startIndex = i
                endIndex = checkComments(inputCode, i)
                checkError(endIndex)
                i = endIndex
                previousState = "inComment"
                currentState = "done"
            elif inputCode[i].isalpha():
                previousState = "start"
                currentState = "inID"
                startIndex = i
                endIndex = isLetters(inputCode, i)
                checkError(endIndex)
                i = endIndex
                previousState = "inID"
                currentState = "done"
            elif inputCode[i].isdigit():
                previousState = "start"
                currentState = "inNum"
                startIndex = i
                endIndex = checkDigits(inputCode, i)
                checkError(endIndex)
                i = endIndex
                previousState = "inNum"
                currentState = "done"
            elif inputCode[i] == ":":
                previousState = "start"
                currentState = "inAssign"
                startIndex = i
                if(inputCode[i + 1] == "="):
                    endIndex = i + 1
                    previousState = "inAssign"
                    currentState = "done"
                    i = i + 2

                else:
                    endIndex = None
                checkError(endIndex)

            elif inputCode[i] in specialChars:
                previousState = "start"
                currentState = "done"
                endIndex = i
                i = i + 1
            else:
                currentState = "done"
        if currentState == "done":
            if previousState == "inID":
                output = inputCode[startIndex:endIndex]
                index = 0
                if output in reservedWords:
                    # TODO replace special symbol with tuple data
                    index = reservedWords.index(output)
                    tokens.append((output, "," + reservedWordsType[index]))
                else:
                    tokens.append((output, ",IDENTIFIER"))
            elif previousState == "inNum":
                output = inputCode[startIndex:endIndex]
                tokens.append((output, ",NUMBER"))
            elif previousState == "inAssign":
                output = inputCode[startIndex: endIndex + 1]
                tokens.append((output, ",ASSIGN"))
            elif previousState == "start":
                output = inputCode[endIndex]
                if output in specialChars:
                    # TODO replace special symbol with tuple data
                    index = specialChars.index(output)
                    tokens.append((output, "," + specialCharsType[index]))
                else:
                    checkError(None)
            currentState = "start"
    return tokens
# f = open("outputFile.txt", "w")
# f.write('\n'.join(tokens))
# f.close()

# print(tokens, file = open('outputFile.txt'))
# tokens = Scan(readData('snippet.txt'))
# writeData('outputTokenFile.txt', tokens)
# print('File Scanned')
# os.system("pause")


# checkComments(""".3{xlolk lp;poe46484} """, 2)
