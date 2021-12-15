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
                print(node)
    if root.sibling:
        print()
        print("---- Sibling of " + str(root.token) + " ----")
        # print(root.sibling)
        Show(root.sibling)
    return


# nodes = []
# edges = []
index = 0
specialChars = ['(', ')', '+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=']
reservedWords = ["if", "then", "else", "end",
                 "repeat", "until", "read", "write"]

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
token = []
tokensInstance = Tokens(token)


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

    resultNode = Node('','')
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
    Show(mynode)
    return mynode


# Run(token)
# def main():
#     # newtokens = [("lol","read")]
#     # Run(tokensInstance.tokens)
#     return

# main()
