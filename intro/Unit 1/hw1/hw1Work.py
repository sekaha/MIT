# Will have to do this from scratch in essence, this OCW doesn't include what I need, and also uses old python
# I'll just be going off of the homework spec  rather than the py file they include.
# I use these assignments as note spaces as well, when I encounter new concepts, anticipate weird comments.

# for functional style
import operator

from numpy import isin

### Syntax Tree Classes
# leaf nodes => are numbers/vars
# internal nodes => are operations (non-terminating nodes! like encountered in linguistics)

# this is a node with optionally two children, hence the name tree
class BinOp:
    def __init__(self,left,right):
        self.left = left
        self.right = right

    # \ tells python to extend the current
    # logic line over to the next physical line
    def __str__(self):
        return f"{self.op_str}({self.left}, {self.right})"

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    # huh, apparently, you can make functions
    # equal to others. OOP :)
    # repr is a printable representation of the object
    __repr__ = __str__

class ArithmeticOp(BinOp):
    op_str = ''
    op = None

    def get_operator(self):
        return self.op

class Sum(ArithmeticOp):
    op_str = 'Sum'
    op = operator.add

class Prod(ArithmeticOp):
    op_str = 'Prod'
    op = operator.mul

class Quot(ArithmeticOp):
    op_str = 'Quot'
    op = operator.truediv

class Diff(ArithmeticOp):
    op_str = 'Diff'
    op = operator.sub

class Assign(BinOp):
    op_str = 'Assign'

class Number:
    def __init__(self,val):
        self.val = val

    def get_val(self):
        return self.val

    def __str__(self):
        return f'Num({self.val})'

    __repr__ = __str__

class Variable:
    def __init__(self,name):
        self.name = name
    
    def get_name(self):
        return self.name

    def __str__(self):
        return f'Var({self.name})'

    __repr__ = __str__

### Tokenizer

# returns a list of tokens
token_types = {"(":None,")":None,"*":Prod,"/":Quot,"+":Sum,"-":Diff,"=":Assign}

def tokenize(input_str):
    input_str = input_str.replace(" ","")
    terminating_value = ""
    tokens = []

    # passing over every character
    while (len(input_str) > 0):
        char = input_str[0]

        # if the token is a known type, add it to the tokens list
        if (char in token_types):
            # check if this is trying to signify a negative value
            if (char == '-') and (terminating_value == "") and \
            (len(input_str) >= 2) and (input_str[1] in "1234567890"):
                terminating_value += char
            else:
                # add variable token name first!
                if terminating_value != "":
                    tokens.append(terminating_value)
                    terminating_value = ""
                tokens.append(char)
        else:
            # if it's not a known type, then it is a variable name/number
            terminating_value += char

        # remove the first character
        input_str = input_str[1::]
    
    # If the last element is a variable name/number, add that
    if terminating_value!="":
        tokens.append(terminating_value)
    
    return tokens

### Parser

# takes a list of tokens, makes a tree with recursive descent
def parse(tokens):
    # every non-terminating expression is (expression op expression)
    def parse_exp(index):
        # returns expression at index, index where expression ends
        current_token = tokens[index]
        current_index = index
        exp = None

        # make number
        if all([(char in "1234567890.-") for char in current_token]):
            exp = Number(float(current_token))
            current_index += 1
        # make binop
        elif (current_token == "("):
            # recursive parse of an expression, left tree
            # get index beyond end of expression
            left_tree, current_index = parse_exp(current_index+1)
            
            # token beyond left tree should be a single-character operator token
            # call it op
            while tokens[current_index] == ")":
                current_index+=1
            
            op = token_types[tokens[current_index]]

            # parse expression, right tree
            right_tree, current_index = parse_exp(current_index+1)

            # use op to make syntax tree with left and right tree
            # return it as a result of the procedure
            # with the index of the token beyond the right paren
            exp = op(left_tree,right_tree)
            
        # make variable name
        else:
            exp = Variable(current_token)
            current_index += 1

        return exp, current_index
    (parsed_exp,next_index) = parse_exp(0)
    return parsed_exp

### Lazy Evaluation

# empty dictionary used to store values
env = {}

def evaluate(exp):
    # handle various expression types based on how they evaluate
    if isinstance(exp,Number):
        return exp.get_val()

    # if expr var, return value associated with name
    if isinstance(exp,Variable):
        if exp.get_name() in env:
            val = env[exp.get_name()]
            if not isinstance(val,float):
                val = evaluate(val)
                env[exp.get_name()] = val
            return val
        else:
            return exp

    # if arthematic operation, return result of applying that operation
    if isinstance(exp,ArithmeticOp):
        operation = exp.get_operator()
        
        left = evaluate(exp.get_left())
        right = evaluate(exp.get_right())

        if isinstance(left,float) and isinstance(right,float):
            return operation(left,right)
        else:
            return type(exp)(left,right)

    # if expr is assignment, evaluate right hand tree
    if isinstance(exp,Assign):
        # lazy evaluation, add unevaluated variable to environment dictionary
        env[exp.get_left().get_name()] = exp.get_right()
        return f"assigned '{exp.get_left().get_name()}'"

# Testing our program :)
while True:
    usr_inp = tokenize(input("ψ "))
    print(evaluate(parse(usr_inp)))