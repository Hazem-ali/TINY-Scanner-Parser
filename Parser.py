from typing import Tuple


class Node:
    def __init__(self, token, sub_token=""):
        self.token = token
        self.sub_token = sub_token
        self.children = []
        self.sibling = None
        # self.index = 0

    def setChild(self, node):
        self.children.append(node)
        # self.index = self.index + 1

    def setSibling(self, sibling):
        self.sibling = sibling

    def __str__(self) -> str:
        if self.sub_token == "":
            return f""""Token: " {str(self.token)}"""

        return f""""Token: " {str(self.token)}
"Sub_Token: " {str(self.sub_token)}"""
        # print("sibling: " + str(self.sibling))


class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens

    def setTokens(self, tokens):
        self.tokens = tokens
        # self.index = self.index + 1


def Show(root: Node):
    if root.sibling is None and root.children == []:
        return
    print(root)
    if root.children != []:
        for node in root.children:
            print()
            print("---- Child of " + str(root.token) + " ----")
            if type(node) == Node:
                Show(node)
            else:
                # print("LOL")
                print(node)
    if root.sibling:
        print()
        print("---- Sibling of " + str(root.token) + " ----")
        # print(root.sibling)
        Show(root.sibling)
    return


# TODO {1 : ( [(1,2), (1,3), (1,4)] , LEVEL, LABEL_NAME, BOOLEAN)}


nodeNumber = 0

# TODO make minus and equal presentation and true/false in dict
def createLabel(mainToken, sub_token):
    # prepare the label for the node
    if sub_token == "":
        return mainToken[1]
    else:
        return mainToken[1] + " (" + sub_token[0] + ")"


def MakeTree(root: Node, treeDict={}, level=0):
    global nodeNumber
    currentNode = nodeNumber
    if type(root) == type(tuple()):
        newNumber = nodeNumber + 1
        treeDict[currentNode] = ([], level, root[1] + " (" + root[0] + ")")
        # newLevel = level + 1
        # treeDict[nodeNumber][0].append((nodeNumber, newNumber))
        # nodeNumber += 1
        return treeDict
    # if root.sibling is None and root.children == []:

    #     newNumber = nodeNumber + 1
    #     # newLevel = level + 1
    #     treeDict[nodeNumber][0].append((nodeNumber, newNumber))
    #     return treeDict

    # print(root)

    treeDict[currentNode] = (
        [], level, createLabel(root.token, root.sub_token))

    if root.children != []:
        # global newNumber
        # newNumber = None
        for node in root.children:

            newNumber = nodeNumber + 1
            newLevel = level + 1
            nodeNumber += 1
            MakeTree(node, treeDict, newLevel)
            treeDict[currentNode][0].append((currentNode, newNumber))

            # if type(node) == Node:
            #     return MakeTree(node, treeDict, newNumber, newLevel)
            # else:
            #     return MakeTree(node, treeDict, newNumber, newLevel)
            #     print(node)

    if root.sibling:
        newNumber = nodeNumber + 1

        nodeNumber += 1
        MakeTree(root.sibling, treeDict, level)
        treeDict[currentNode][0].append((currentNode, newNumber))
    return treeDict


index = 0
token = []
specialChars = ['(', ')', '+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=']
specialCharsTuple = [('(', "OPENBRACKET"), (')', "CLOSEDBRACKET"), ('+', "PLUS"), ('-', "MINUS"), ('*', "MULT"), ('/', "DIV"),
                     ('=', "EQUAL"), (';', "SEMICOLON"), ('<', "LESSTHAN"), ('>', "GREATERTHAN"), ('<=', "LESSTHANOREQUAL"), ('<=', "GREATERTHANOREQUAL")]
reservedWords = ["if", "then", "else", "end",
                 "repeat", "until", "read", "write"]
reservedWordsTuple = [("if", "IF"), ("then", "THEN"), ("else", "ELSE"), ("end", "END"),
                      ("repeat", "REPEAT"), ("until", "UNTIL"), ("read", "READ"), ("write", "WRITE")]
tokensInstance = Tokens(token)
sample = {1: ([(1, 2)], 0, "('read', 'READ'): ('x', 'IDENTIFIER')"),
          2: ([(2, 3), (2, 6)], 0, "('if', 'IF'): "),
          3: ([(3, 4), (3, 5)], 1, "('<', 'LESSTHAN'): "),
          4: ([], 2, "('0', 'NUMBER')"),
          5: ([], 2, "('x', 'IDENTIFIER')"),
          6: ([(6, 7), (6, 8)], 1, "(':=', 'ASSIGN'): ('fact', 'IDENTIFIER')"),
          7: ([], 2, "('1', 'number')"),
          8: ([(8, 9), (8, 17), (8, 20)], 1, "('repeat', 'REPEAT'): "),
          9: ([(9, 10), (9, 13)], 2, "(':=', 'ASSIGN'): ('fact', 'IDENTIFIER')"),
          10: ([(10, 11), (10, 12)], 3, "('*', 'MULT'): "),
          11: ([], 4, "('fact', 'IDENTIFIER')"),
          12: ([], 4, "('x', 'IDENTIFIER')"),
          13: ([(13, 14)], 2, "(':=', 'ASSIGN'): ('x', 'IDENTIFIER')"),
          14: ([(14, 15), (14, 16)], 3, "('-', 'MINUS'): "),
          15: ([], 4, "('x', 'IDENTIFIER')"),
          16: ([], 4, "('1', 'NUMBER')"),
          17: ([(17, 18), (17, 19)], 2, "('=', 'EQUAL'): "),
          18: ([], 3, "('x', 'IDENTIFIER')"),
          19: ([], 3, "('0', 'NUMBER')"),
          20: ([(20, 21)], 1, "('write', 'WRITE'): "),
          21: ([], 2, "('fact', 'IDENTIFIER')")}

sample2 = {1: ([(1, 2)], 0, 'READ (x)')
, 2: ([(2, 3), (2, 6)], 0, 'IF'),
 3: ([(3, 4), (3, 5)], 1, 'LESSTHAN'),
  4: ([], 2, 'NUMBER (0)'), 
  5: ([], 2, 'IDENTIFIER (x)'), 
  6: ([(6, 7), (6, 8)], 1, 'ASSIGN (fact)'), 
  7: ([], 2, 'number (1)'), 
  8: ([(8, 9), (8, 17), (8, 20)], 1, 'REPEAT'), 
  9: ([(9, 10), (9, 13)], 2, 'ASSIGN (fact)'), 
  10: ([(10, 11), (10, 12)], 3, 'MULT'), 
  11: ([], 4, 'IDENTIFIER (fact)'), 
  12: ([], 4, 'IDENTIFIER (x)'),
   13: ([(13, 14)], 2, 'ASSIGN (x)'), 
   14: ([(14, 15), (14, 16)], 3, 'MINUS'), 
   15: ([], 4, 'IDENTIFIER (x)'),
    16: ([], 4, 'NUMBER (1)'), 
    17: ([(17, 18), (17, 19)], 2, 'EQUAL'), 
    18: ([], 3, 'IDENTIFIER (x)'), 
    19: ([], 3, 'NUMBER (0)'), 
    20: ([(20, 21)], 1, 'WRITE'), 
    21: ([], 2, 'IDENTIFIER (fact)')}

# tokenType = ["SEMICOLON", "IF", "THEN", "END", "REPEAT", "UNTIL", "IDENTIFIER", "ASSIGN", "READ", "WRITE", "LESSTHAN", "EQUAL","PLUS", "MINUS", "MULT", "DIV", "OPENBRACKET", "CLOSEDBRACKET", "NUMBER"]
# tokenValue = [';','if','then', 'end', 'repeat', 'until' , ':=', 'read', 'write', '<','=', '+', '-','*', '/', '(', ')']
# token = [('read', "read"), ('x', "identifier"), (';', "SEMICOLON"), ('if', "if"), ('(', "OPENBRACKET"), ('0', "number"), ('<', "LESSTHAN"), ('x', "identifier"), (')', "CLOSEDBRACKET"), ('then', "then"),
#          ('fact', "identifier"), (':=', "assign"), ('result',
#                                                     "identifier"), (';', "SEMICOLON"), ('repeat', "repeat"),
#          ('fact', "identifier"), (':=', "assign"), ('fact',
#                                                     "identifier"), ('*', "mult"), ('x', "identifier"), (';', "SEMICOLON"),
#          ('x', "identifier"), (':=', "assign"), ('x', "identifier"), ('-',
#                                                                       "minus"), ('1', "number"), ('until', "until"),
#          ('x', "identifier"), ('=', "equal"), ('0',
#                                                "number"), (';', "SEMICOLON"), ('write', "write"),
#          ('fact', "identifier"), ('end', "end")]

# token = [('read', 'READ'), ('x', 'IDENTIFIER'), (';', 'SEMICOLON'), ('if', 'IF'), ('0', 'NUMBER'), ('<', 'LESSTHAN'), ('x', 'IDENTIFIER'), ('then', 'THEN'), ('fact', 'IDENTIFIER'), (':=', 'ASSIGN'), (';', 'SEMICOLON'), ('repeat', 'REPEAT'), ('fact', 'IDENTIFIER'), (':=', 'ASSIGN'), ('fact', 'IDENTIFIER'), ('*', 'MULT'), ('x', 'IDENTIFIER'), (';', 'SEMICOLON'), ('x', 'IDENTIFIER'), (':=', 'ASSIGN'), ('x', 'IDENTIFIER'), ('-', 'MINUS'), ('1', 'NUMBER'), ('until', 'UNTIL'), ('x', 'IDENTIFIER'), ('=', 'EQUAL'), ('0', 'NUMBER'), (';', 'SEMICOLON'), ('write', 'WRITE'), ('fact', 'IDENTIFIER'), ('end', 'END')]


def match(expectedToken):
    global index
    token_val, token_type = tokensInstance.tokens[index]
    # passes over ["SEMICOLON", "IF", "THEN", "END", "REPEAT", "UNTIL", "ASSIGN", "READ", "WRITE", "LESSTHAN", "EQUAL","PLUS", "MINUS", "MULT", "DIV", "OPENBRACKET", "CLOSEDBRACKET"]
    if(token_val == expectedToken):
        index = index + 1
        return tokensInstance.tokens[index - 1]

    # IDENTIFIER
    elif((token_val not in reservedWords) and (token_type.lower() == "identifier")):
        index = index + 1
        return tokensInstance.tokens[index - 1]

    # NUMBER
    elif(token_type.lower() == "number"):
        try:
            tmp = int(token_val)
            index = index + 1
            return tokensInstance.tokens[index - 1]

        except:
            # TODO make an error
            # error matching
            # EXIT UPPER FUNCTION
            return "ERROR"
    else:
        # TODO make an error
        # error matching
        # EXIT UPPER FUNCTION
        return "ERROR"


def assignStatement():
    idToken = match('identifier')
    assignToken = match(':=')

    assignNode = Node(assignToken, idToken)
    assignNode.setChild(exp())
    # print(assignNode)
    return assignNode


def writeStatement():
    # same as print
    writeNode = Node(tokensInstance.tokens[index])
    match('write')
    writeNode.setChild(exp())
    return writeNode


def factor():
    if(tokensInstance.tokens[index][0] == '('):
        match('(')
        # exp()
        match(')')
    elif(tokensInstance.tokens[index][1].lower() == 'number'):
        return match('number')
    elif(tokensInstance.tokens[index][1].lower() == 'identifier'):
        return match('identifier')


def stmt_sequence():
    stmt_sequenceNode = statement()
    # statement()
    i = 0
    rootNode = Node('', '')
    tmpNode = stmt_sequenceNode

    while(tokensInstance.tokens[index][0] == ';'):
        match(tokensInstance.tokens[index][0])
        sibling = statement()
        tmpNode.setSibling(sibling)
        stmt_sequenceNode = tmpNode
        tmpNode = sibling
        if i == 0:
            rootNode = stmt_sequenceNode
            i = i + 1

    return rootNode


def statement():

    resultNode = Node('', '')
    if(tokensInstance.tokens[index][1].lower() == "identifier"):
        resultNode = assignStatement()
    elif(tokensInstance.tokens[index][1].lower() == "if"):
        resultNode = ifStatement()
    elif(tokensInstance.tokens[index][1].lower() == "repeat"):
        resultNode = repeat()
    elif(tokensInstance.tokens[index][1].lower() == "read"):
        resultNode = readStatement()
    elif(tokensInstance.tokens[index][1].lower() == "write"):
        resultNode = writeStatement()

    return resultNode


def repeat():
    repeatNode = Node(tokensInstance.tokens[index])
    match('repeat')
    child1 = stmt_sequence()
    repeatNode.setChild(child1)
    match('until')
    child2 = exp()
    repeatNode.setChild(child2)
    return repeatNode


def ifStatement():
    node = Node(tokensInstance.tokens[index])
    match('if')
    if tokensInstance.tokens[index][0] == '(':
        match('(')
    child1 = exp()
    node.setChild(child1)
    if tokensInstance.tokens[index][0] == ')':
        match(')')
    match('then')
    child2 = stmt_sequence()
    node.setChild(child2)
    if (tokensInstance.tokens[index][1].lower() == 'else'):
        match('else')
        child3 = stmt_sequence()
        node.setChild(child3)
    return node


def readStatement():

    # success
    readToken = match('read')
    idToken = match('identifier')
    readNode = Node(readToken, idToken)
    # print(readNode)
    return readNode


def exp():
    node1 = simpleExp()
    newNode = node1
    while tokensInstance.tokens[index][0] == '<' or tokensInstance.tokens[index][0] == '=' or tokensInstance.tokens[index][0] == '>':
        newNode = Node(tokensInstance.tokens[index])
        match(tokensInstance.tokens[index][0])
        newNode.setChild(node1)
        node2 = simpleExp()
        newNode.setChild(node2)
    return newNode


def simpleExp():
    tempNode1 = term()
    while tokensInstance.tokens[index][0] == '+' or tokensInstance.tokens[index][0] == '-':
        newTemp = Node(tokensInstance.tokens[index])
        match(tokensInstance.tokens[index][0])
        newTemp.setChild(tempNode1)
        tempNode2 = term()
        newTemp.setChild(tempNode2)
        tempNode1 = newTemp
    return tempNode1


def term():
    tempNode1 = factor()
    while tokensInstance.tokens[index][0] == '*':
        newTemp = Node(tokensInstance.tokens[index])
        match(tokensInstance.tokens[index][0])
        newTemp.setChild(tempNode1)
        tempNode2 = factor()
        newTemp.setChild(tempNode2)
        tempNode1 = newTemp
    return tempNode1


def Run(token_tuples):
    tokensInstance.setTokens(token_tuples)
    mynode = stmt_sequence()
    # Show(mynode)
    return mynode


# Run(token)
# def main():
#     # newtokens = [("lol","read")]
#     # Run(tokensInstance.tokens)
#     return

# main()
