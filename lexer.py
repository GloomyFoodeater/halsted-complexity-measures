# Lexem patterns for regular expressions
ignore = r'//.*\n|/\*(.|\n)*\*/|\s'
keyword = r'break|case|catch|class|const|continue|debugger|default|delete|do|'\
'else|enum|export|extends|false|finally|\for|function|if|import|in|instanceof|'\
'new|null|return|super|switch|this|throw|true|try|typeof|var|void|while|with|'\
'as|implements|interface|let|package|private|protected|public|static|yield|'\
'any|boolean|constructor|declare|get|module|require|number|set|string|symbol|'\
'type|from|of'
literal = r'/([^/\\]|\\.)*/[gimy]{0,4}|'\
r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|`([^`\\]|\\.)*`|'\
r'\d+[eE][+-]?\d+|\d*\.\d+|(0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+)n?'
identifier = r'[a-zA-Z_$][a-zA-Z_$\d]*'
operator = r'>>>=|>>>|>>=|===|<<=|!==|\|\||\|=|\^=|\?\?|>>|>=|==|<=|<<|/=|'\
r'\.\?|-=|--|\+=|\+\+|\*=|\*\*|&=|&&|%=|!=|~|\||\^|\?|>|=|<|/|-|\+|\*|&|%|!|\.';
delimiter = r';|:|\)|\(|\}|\{|\]|\[|,'

def tokenize(src):    
    '''Function for splitting code into tokens
    This function allows to split source code written in TypeScript language
    into list of tokens. Token format is a tuple: 1st element - lexem type,
    2nd element - lexem.

    Input:
        src - source code in TypeScript.
        
    Output:
        List of tokens.
    '''

    # Init output list for tokens
    tokens = [] 
    
    # Init list with regular expressions
    regexes = [re.compile(ignore), re.compile(keyword), re.compile(literal),
               re.compile(identifier), re.compile(operator), re.compile(delimiter)]
    
    # Init current position and length of source code
    p = 0
    n = len(src)
    
    # Iterate over sorce code
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
            # TODO 2: Check regex literals
                tokens.append((i, match.group(0)))
                p = match.end()
                break
        # TODO 1: Add raising error when out of array and doesn't match
    return tokens