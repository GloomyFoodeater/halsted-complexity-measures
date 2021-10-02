keyword = r'break|case|catch|class|const|continue|debugger|default|delete|do|'\
'else|enum|export|extends|false|finally|\for|function|if|import|in|instanceof|'\
'new|null|return|super|switch|this|throw|true|try|typeof|var|void|while|with|'\
'as|implements|interface|let|package|private|protected|public|static|yield|'\
'any|boolean|constructor|declare|get|module|require|number|set|string|symbol|'\
'type|from|of'

literal = r'/([^/\\]|\\.)*/[gimy]{0,4}|'\
r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|`([^`\\]|\\.)*`|'\
r'\d+[eE][+-]?\d+|\d*\.\d+|(0x[\da-fA-F]+|0o[0-7]+|0b[01]+|\d+)n?'


identifier = r'[a-zA-Z_$][a-zA-Z_$\d]'

operator = r'>>>=|>>>|>>=|===|<<=|!==|\|\||\|=|\^=|\?\?|>>|>=|==|<=|<<|/=|'\
r'\.\?|-=|--|\+=|\+\+|\*=|\*\*|&=|&&|%=|!=|~|\||\^|\?|>|=|<|/|-|\+|\*|&|%|!|\.';

delimiter = r';|:|\)|\(|\}|\{|\]|\[|,'