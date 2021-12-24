

class Node:
    def __init__(self, token, sub_token=""):
        self.token = token
        self.sub_token = sub_token
        self.children = []
        self.sibling = None

    def setChild(self, node):
        self.children.append(node)


    def setSibling(self, sibling):
        self.sibling = sibling

    def __str__(self) -> str:
        if self.sub_token == "":
            return f""""Token: " {str(self.token)}"""

        return f""""Token: " {str(self.token)}
"Sub_Token: " {str(self.sub_token)}"""



class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens

    def setTokens(self, tokens):
        self.tokens = tokens



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
                print(node)
    if root.sibling:
        print()
        print("---- Sibling of " + str(root.token) + " ----")
        Show(root.sibling)
    return





nodeNumber = 1
error = None




def createLabelAndBox(mainToken, sub_token):

    specialCharsTuple = [('(', "OPENBRACKET"), (')', "CLOSEDBRACKET"), ('+', "PLUS"), ('-', "MINUS"), ('*', "MULT"), ('/', "DIV"),
                         ('=', "EQUAL"), (';', "SEMICOLON"), ('<', "LESSTHAN"), ('>', "GREATERTHAN"), ('<=', "LESSTHANOREQUAL"), ('<=', "GREATERTHANOREQUAL")]
    label = ''
    box = 'square'
    # prepare the label for the node
    if sub_token == "":
        if mainToken in specialCharsTuple:
            # then it's an operation
            label = mainToken[1] + " (" + mainToken[0] + ")"
            box = 'circle'
        else:
            # Then it's a reserved Word with no sub_token like if, repeat
            try:
                label = mainToken[1]
            except:
                label = mainToken

    else:
        # Then it's assign or read or write
        label = mainToken[1] + " (" + sub_token[0] + ")"

    return label, box


def MakeTree(root: Node, treeDict={}, level=0):
    global nodeNumber
    currentNode = nodeNumber
    # Base Case
    if type(root) == type(tuple()):
        newNumber = nodeNumber + 1
        treeDict[currentNode] = (
            [], level, root[1] + " (" + root[0] + ")", 'circle')
        return treeDict
    

    # Creating a label and box for incoming token  
    print(root)
    if root is None:
        error = "Wrong Syntax"
        return
    label, box = createLabelAndBox(root.token, root.sub_token)
    if label !='':
        treeDict[currentNode] = ([], level, label, box)

    # Starting from children
    if root.children != []:
        for node in root.children:

            newNumber = nodeNumber + 1
            newLevel = level + 1
            nodeNumber += 1
            MakeTree(node, treeDict, newLevel)
            treeDict[currentNode][0].append((currentNode, newNumber))

    # Going to siblings
    if root.sibling:
        newNumber = nodeNumber + 1

        nodeNumber += 1
        MakeTree(root.sibling, treeDict, level)
        treeDict[currentNode][0].append((currentNode, newNumber))

    return treeDict


index = 0
token = []
specialChars = ['(', ')', '+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=']

reservedWords = ["if", "then", "else", "end",
                 "repeat", "until", "read", "write"]
reservedWordsTuple = [("if", "IF"), ("then", "THEN"), ("else", "ELSE"), ("end", "END"),
                      ("repeat", "REPEAT"), ("until", "UNTIL"), ("read", "READ"), ("write", "WRITE")]
tokensInstance = Tokens(token)



sample = {1: ([(1, 2)], 0, 'READ (x)', 'square'),
           2: ([(2, 3), (2, 6)], 0, 'IF', 'square'),
           3: ([(3, 4), (3, 5)], 1, 'LESSTHAN (<)', 'circle'),
           4: ([], 2, 'NUMBER (0)', 'circle'),
           5: ([], 2, 'IDENTIFIER (x)', 'circle'),
           6: ([(6, 7), (6, 8)], 1, 'ASSIGN (fact)', 'square'),
           7: ([], 2, 'number (1)', 'circle'),
           8: ([(8, 9), (8, 17), (8, 20)], 1, 'REPEAT', 'square'),
           9: ([(9, 10), (9, 13)], 2, 'ASSIGN (fact)', 'square'),
           10: ([(10, 11), (10, 12)], 3, 'MULT (*)', 'circle'),
           11: ([], 4, 'IDENTIFIER (fact)', 'circle'),
           12: ([], 4, 'IDENTIFIER (x)', 'circle'),
           13: ([(13, 14)], 2, 'ASSIGN (x)', 'square'),
           14: ([(14, 15), (14, 16)], 3, 'MINUS (-)', 'circle'),
           15: ([], 4, 'IDENTIFIER (x)', 'circle'),
           16: ([], 4, 'NUMBER (1)', 'circle'),
           17: ([(17, 18), (17, 19)], 2, 'EQUAL (=)', 'circle'),
           18: ([], 3, 'IDENTIFIER (x)', 'circle'),
           19: ([], 3, 'NUMBER (0)', 'circle'),
           20: ([(20, 21)], 1, 'WRITE', 'square'),
           21: ([], 2, 'IDENTIFIER (fact)', 'circle')}

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
    global error
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
            error = "Non-Integer Value"
            return error
    else:
        # TODO make an error
        # error matching
        # EXIT UPPER FUNCTION
        error = "Invalid Token Type"
        return error


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
        node = exp()
        match(')')
        return node
    elif(tokensInstance.tokens[index][1].lower() == 'number'):
        return match('number')
    elif(tokensInstance.tokens[index][1].lower() == 'identifier'):
        return match('identifier')


def stmt_sequence():
    stmt_sequenceNode = statement()
    # statement()
    i = 0
    rootNode = stmt_sequenceNode
    tmpNode = stmt_sequenceNode
    try:
        while(tokensInstance.tokens[index][0] == ';'):
            match(tokensInstance.tokens[index][0])
            sibling = statement()
            tmpNode.setSibling(sibling)
            stmt_sequenceNode = tmpNode
            tmpNode = sibling
            if i == 0:
                rootNode = stmt_sequenceNode
                i = i + 1
    except:
        pass

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
    else:
        error = "Invalid Tokens"

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
    match("end")
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
    try:
        while tokensInstance.tokens[index][0] == '<' or tokensInstance.tokens[index][0] == '=' or tokensInstance.tokens[index][0] == '>':
            newNode = Node(tokensInstance.tokens[index])
            match(tokensInstance.tokens[index][0])
            newNode.setChild(node1)
            node2 = simpleExp()
            newNode.setChild(node2)
    except:
        pass
    return newNode


def simpleExp():
    tempNode1 = term()

    try:
        while tokensInstance.tokens[index][0] == '+' or tokensInstance.tokens[index][0] == '-':
            newTemp = Node(tokensInstance.tokens[index])
            match(tokensInstance.tokens[index][0])
            newTemp.setChild(tempNode1)
            tempNode2 = term()
            newTemp.setChild(tempNode2)
            tempNode1 = newTemp
    except:
        pass
    
    
    return tempNode1


def term():
    tempNode1 = factor()

    try:
        while tokensInstance.tokens[index][0] == '*' or tokensInstance.tokens[index][0] == '/':
            newTemp = Node(tokensInstance.tokens[index])
            match(tokensInstance.tokens[index][0])
            newTemp.setChild(tempNode1)
            tempNode2 = factor()
            newTemp.setChild(tempNode2)
            tempNode1 = newTemp
    except:
        pass
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
