import re

# Token class
class Token:
    def __init__(self, type, value, name):
        self.type = type
        self.value = value
        self.name = name

    @property
    def is_operand(self):
        is_literal = self.type == 2 or self.value in ['true', 'false', 'null']
        is_variable = self.type == 4
        return is_literal or is_variable or self.value == 'this'
    
    @property
    def is_operator(self):
        is_function = self.type == 3
        is_ts_operator = self.type == 5 or self.value in ['break', 
        'continue', 'debugger', 'delete', 'do', 'for', 'if', 'else', 'in', 
        'instanceof', 'new', 'return', 'switch', 'throw', 'try', 'catch', 
        'finally', 'typeof', 'void', 'while', 'with', 'as', 'yield']
        is_delimiter = self.type == 6
        return is_function or is_ts_operator or is_delimiter

# Exception class for tokenize function
class InputError(Exception):
    def __init__(self, msg, src, pos):
        self.message = msg
        self.src = src
        self.line = 1
        self.column = 1
        for i in range(0, pos):
            if src[i] == '\n':
                self.line += 1
                self.column = 0
            self.column += 1


# Function to split source code into tokens
def tokenize(src):    
    # Lexem patterns for regular expressions
    patterns = []
    patterns.append(r'\n?\s*["\'`]use strict["\'`];?\n|//.*\n|/\*(.|\n)*\*/|\s')
    patterns.append('(break|case|catch|class|const|continue|debugger|default|'\
    'delete|do|else|enum|export|extends|false|finally|for|function|if|'\
    'import|in|instanceof|new|null|return|super|switch|this|throw|true|'\
    'try|typeof|var|void|while|with|as|implements|interface|let|package|'\
    'private|protected|public|static|yield|any|boolean|constructor|'\
    'declare|get|module|require|number|set|string|symbol|type|from|of)'\
    r'(?![\da-zA-Z_$])')
    patterns.append(r'/([^/\\]|\\.)+/[gimy]{0,4}|'\
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|`([^`\\]|\\.)*`|'\
    r'\d+[eE][+-]?\d+|\d*\.\d+|(0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+)n?|'\
    r'undefined')
    patterns.append(r'[a-zA-Z_$][a-zA-Z_$\d]*\s*\(')
    patterns.append(r'[a-zA-Z_$][a-zA-Z_$\d]*')
    patterns.append(r'>>>=|>>>|>>=|===|<<=|!==|\|\||\|=|\^=|\?\?|>>|>=|==|<=|'\
    r'<<|/=|\.\?|!\.|-=|--|\+=|\+\+|\*=|\*\*|&=|&&|%=|!=|~|\||\^|'\
    r'\?(?![:)=,])|>|=|<|/|-|\+|\*|&|%|!|\.')
    patterns.append(r';|:|\)|\(|\}|\{|\]|\[|,|=>|\?')
    
    # Init token list and regex list
    tokens = [] 
    regexes = []
    for i in range(len(patterns)):
        regexes.append(re.compile(patterns[i]))

    for_in_checker = re.compile(r'for\s*\(\s*(var|let)\s+[a-zA-Z_$][a-zA-Z_$\d]*\s+in')

    # Iterate over sorce code
    p = 0 # Current position
    while (p < len(src)):
        # Exclude comments and space characters
        match = regexes[0].match(src, pos = p)
        if match:
            p = match.end()
            continue
        
        # Try to match any lexem
        for i in range(1, len(regexes)):
            match = regexes[i].match(src, pos = p)
            if match:
                # Get found match
                token_value = match.group(0) 

                # Decorate token name to discern between similiar operators
                if token_value == 'for' and for_in_checker.match(src, pos = p):
                    token_name = 'for/in(...)'
                elif token_value == 'for':
                    token_name = 'for(...;...;...)'
                elif token_value == 'while':
                    token_name = 'while(...)'
                elif token_value == 'do':
                    token_name = 'do{...}while(...)'
                elif token_value == '?' and i == 5:
                    token_name = '...?...:...'
                elif token_value == '(':
                    token_name = '(...)'
                elif token_value == '[':
                    token_name = '[...]'
                elif token_value == '{':
                    token_name = '{...}'
                elif token_value == 'if':
                    token_name = 'if(...)'
                elif token_value == 'switch':
                    token_name = 'switch(...){...}'
                elif token_value in ['try', 'catch', 'finally']:
                    token_name = token_value + '{...}'
                elif i == 3:
                    token_value = token_value[:-1]
                    token_name = token_value + '(...)'
                else:
                    token_name = token_value

                # Discern between ts regex syntax and double division: 
                if i == 2 and token_value[0] == '/' and tokens != [] and not (tokens[-1].value in '=,;:([{'):
                    continue # Previous symbol could be an operand
                tokens.append(Token(i, token_value, token_name))
                p = match.end()
                if i == 3:
                    p -= 1
                break
        else:
            # Error if matches not found
            raise InputError("Characters don't match any known lexem.", src, p)
    return tokens