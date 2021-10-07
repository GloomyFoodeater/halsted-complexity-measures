from lexer import tokenize, Token

def rm_from_dict(dictionary, key):
    if key in dictionary:
        del dictionary[key]

def put_to_dict(dictionary, key):    
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

def take_from_dict(dictionary, key, count = 1):
    if key in dictionary:
        dictionary[key] -= count
    else:
        dictionary[key] = -count

def correct_dict(dictionary):

    # Correct complex operators
    for key, counter in dictionary.copy().items():
        if key == '(...)':
            rm_from_dict(dictionary, ')')
        elif key == '[...]':
            rm_from_dict(dictionary, ']')
        elif key == '{...}':
            rm_from_dict(dictionary, '}')
        elif key == 'for/in(...)':
            take_from_dict(dictionary, '(...)', counter)
            take_from_dict(dictionary, 'in', counter)
        elif key in ['for(...)', 'while(...)', 'if(...)']:
            take_from_dict(dictionary, '(...)', counter)
        elif key == '...?...:...':
            take_from_dict(dictionary, ':', counter)
        elif key == 'switch(...){...}':
            take_from_dict(dictionary, '(...)', counter)
            take_from_dict(dictionary, '{...}', counter)
        elif key in ['try{...}', 'catch{...}', 'finally{...}']:
            take_from_dict(dictionary, '{...}', counter)
        elif key == 'do{...}while(...)':
            take_from_dict(dictionary, 'while(...)', counter)
            take_from_dict(dictionary, '{...}', counter)
        elif key[-5:] == '(...)':
            take_from_dict(dictionary, '(...)', counter)

    # Remove not existing operators
    for key, counter in dictionary.copy().items():
        if counter <= 0:
            del dictionary[key]

# Class for counting Holsted measures
class HolstedMeasures:
    def __init__(self, src):
        self._tokens = tokenize(src)
        print([token.value for token in self._tokens])
        self.operands = {}
        self.operators = {}
        self._fill_vocabulary()
        correct_dict(self.operators)

    def _fill_vocabulary(self):
        i = 0
        while i < len(self._tokens):
            # Get all assignments from var/let/const statement
            if self._tokens[i].value in ['var', 'const', 'let']:
                i = self._parse_var_statement(i + 1)
            
            # Ignore import statements and type assignments
            if self._tokens[i].value in ['type', 'import']:
                while self._tokens[i].value != ';':
                    i += 1
            # Get all delimiters from function header
            if self._tokens[i].value == 'function':
                i = self._parse_func_header(i + 1)

            # Delete var/let/const keyword to escape var/let/const statement
            if self._tokens[i].name == 'for/in(...)':
                del self._tokens[i + 2] 

            # Put token to dictionary
            if self._tokens[i].is_operand:
                put_to_dict(self.operands, self._tokens[i].name)
            elif self._tokens[i].is_operator:
                put_to_dict(self.operators, self._tokens[i].name)
            i += 1

    def _parse_func_header(self, i):
        while self._tokens[i].value != '{':
            if self._tokens[i].is_operator:
                put_to_dict(self.operators, self._tokens[i].name)
            i += 1
        take_from_dict(self.operators, '{...}')
        return i

    def _parse_var_statement(self, i):
            identifier = ''
            while self._tokens[i].value != ';':
                if self._tokens[i].type == 4:
                    identifier = self._tokens[i] # Save new variable
                elif self._tokens[i].value in [':', ',']:
                    put_to_dict(self.operators, self._tokens[i].name) # Save delimiter

                # Check whether there is an initialization
                if self._tokens[i].value in ':=':

                    # Skip until next delimiter
                    while not self._tokens[i].value in '=,;':
                        i += 1

                    # Exit loop if semicolon was found
                    if self._tokens[i].value == ';':
                        break;
                    
                    # Parse expression after =
                    if self._tokens[i].value == '=':
                        put_to_dict(self.operands, identifier.name)
                        put_to_dict(self.operators, self._tokens[i].name)
                        i += 1
                        while not self._tokens[i].value in ';,':
                            if self._tokens[i].is_operand:
                                put_to_dict(self.operands, self._tokens[i].name)
                            elif self._tokens[i].is_operator:
                                put_to_dict(self.operators, self._tokens[i].name)
                            i += 1
                        i -= 1 # To start outer loop with the last token
                i += 1
            
            # Put semicolon to dictionary
            put_to_dict(self.operators, self._tokens[i].name)
            return i + 1