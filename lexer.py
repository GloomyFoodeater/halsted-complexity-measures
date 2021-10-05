import re

class Token:
    def __init__(self, type, value):
        self._type = type
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @property
    def is_literal(self):
        return self._type == 2 or self._value in ['true', 'false', 'null']
    
    @property
    def is_identifier(self):
        return self._type == 3 or self._value == 'this'
    
    @property
    def is_operator(self):
        return self._type == 4 or self._value in ['break', 'continue',
        'debugger', 'delete', 'do', 'for', 'if', 'else', 'in', 'instanceof', 'new', 
        'return', 'switch', 'throw', 'try', 'catch', 'finally', 'typeof', 'void',
        'while', 'with', 'as', 'yield']
    
    @property
    def is_delimiter(self):
        return self._type == 5

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
    patterns.append(r'//.*\n|/\*(.|\n)*\*/|\s')
    patterns.append('break|case|catch|class|const|continue|debugger|default|'\
    'delete|do|else|enum|export|extends|false|finally|for|function|if|'\
    'import|in|instanceof|new|null|return|super|switch|this|throw|true|'\
    'try|typeof|var|void|while|with|as|implements|interface|let|package|'\
    'private|protected|public|static|yield|any|boolean|constructor|'\
    'declare|get|module|require|number|set|string|symbol|type|from|of')
    patterns.append(r'/([^/\\]|\\.)+/[gimy]{0,4}|'\
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|`([^`\\]|\\.)*`|'\
    r'\d+[eE][+-]?\d+|\d*\.\d+|(0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+)n?|undefined')
    patterns.append(r'[a-zA-Z_$][a-zA-Z_$\d]*')
    patterns.append(r'>>>=|>>>|>>=|===|<<=|!==|\|\||\|=|\^=|\?\?|>>|>=|==|<=|<<|/=|'\
    r'\.\?|\.!|-=|--|\+=|\+\+|\*=|\*\*|&=|&&|%=|!=|~|\||\^|\?(?![:)=,])|>|=|<|/|-|\+|\*|&|%|!|\.')
    patterns.append(r';|:|\)|\(|\}|\{|\]|\[|,|=>|?')
    
    # Init token list and regex list
    tokens = [] 
    regexes = []
    for i in range(0, len(patterns)):
        regexes.append(re.compile(patterns[i]))
    
    # Iterate over sorce code
    p = 0 # Current position
    n = len(src) # Source length
    while (p < n):
        # Exclude comments and space characters
        match = regexes[0].match(src, pos = p)
        if match:
            p = match.end()
            continue
        
        # Try to match any lexem
        for i in range(1, len(regexes)):
            match = regexes[i].match(src, pos = p)
            if match:
                token_value = match.group(0)
                # Discern between ts regex syntax and double division: 
                if (i == 2) & (token_value[0] == '/') & (tokens != []):
                    if not (tokens[-1][1] in '=,;:([{'):
                        continue # Previous symbol could be an operand
                tokens.append(Token(i, token_value))
                p = match.end()
                break
        else:
            # Error if matches not found
            raise InputError('Characters do not match any known lexem.', src, p)
    return tokens