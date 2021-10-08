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
        elif key in ['for(...)', 'while(...)', 'if(...)else']:
            take_from_dict(dictionary, '(...)', counter)
        elif key == '...?...:...':
            take_from_dict(dictionary, ':', counter)
        elif key == 'switch(...){...}':
            take_from_dict(dictionary, '(...)', counter)
            take_from_dict(dictionary, '{...}', counter)
        elif key in ['try/catch/finally', 'catch', 'finally']:
            take_from_dict(dictionary, '{...}', counter)
        elif key == 'do{...}while(...)':
            take_from_dict(dictionary, 'while(...)', counter)
            take_from_dict(dictionary, '{...}', counter)
        elif key[-5:] == '(...)':
            take_from_dict(dictionary, '(...)', counter)
        rm_from_dict(dictionary, 'catch')
        rm_from_dict(dictionary, 'finally')

    # Remove not existing operators
    for key, counter in dictionary.copy().items():
        if counter <= 0:
            del dictionary[key]

# Class for counting Holsted measures
class HolstedMeasures:
    def __init__(self, src):
        self._tokens = tokenize(src)
        self.operands = {}
        self.operators = {}
        self._parse_block(0)
        correct_dict(self.operators)

    # Method to parse a block of code
    def _parse_block(self, i):
        braces_balance = 1

        # Iterate over tokens while block is open 
        while braces_balance > 0 and i < len(self._tokens):

            # Change braces balance
            if self._tokens[i].value == '{':
                braces_balance += 1
            elif self._tokens[i].value == '}':
                braces_balance -= 1

            # Parse var/let/const statements
            if self._tokens[i].value in ['var', 'const', 'let']:
                i = self._parse_var_statement(i)
                continue
            
            # Ignore utility statements
            if self._tokens[i].value in ['type', 'import', 'declare'] or self._tokens[i].value == 'export' and self._tokens[i+1].value in '{*=':
                while self._tokens[i].value != ';':
                    i += 1
                i += 1
                continue

            # Parse function expression
            if self._tokens[i].value == 'function':
                i = self._parse_function_expression(i)
                continue

            # Delete var/let/const keyword to escape var/let/const statement
            if self._tokens[i].name == 'for/in(...)':
                del self._tokens[i + 2] 

            # Put token to dictionary
            if self._tokens[i].is_operand:
                put_to_dict(self.operands, self._tokens[i].name)
            elif self._tokens[i].is_operator:
                put_to_dict(self.operators, self._tokens[i].name)

            # Skip error variable declaration during catch block
            if self._tokens[i].value == 'catch' and self._tokens[i + 1].value == '(':
                i += 3
            i += 1
        
        #  Return next token after }    
        return i

    # Method to parse function expression
    def _parse_function_expression(self, i):
        parentheses_balance = 0
        
        # Iterate over parameter list
        while parentheses_balance > 0 or self._tokens[i].value != '{':

            # Change parentheses balance
            if self._tokens[i].value == '(':
                parentheses_balance += 1
            elif self._tokens[i].value == ')':
                parentheses_balance -= 1
            i += 1
        
        # Put braces to vocabulary    
        put_to_dict(self.operators, self._tokens[i].name)
        i += 1
        
        # Parse function body
        i = self._parse_block(i)

        # Return next token after }
        return i 

    # Method to parse var/let/const statements
    def _parse_var_statement(self, i):
            identifier = ''

            # Iterate over statement's tokens
            while self._tokens[i].value != ';':

                # Remember variable id and save delimiters
                if self._tokens[i].type == 4:
                    identifier = self._tokens[i]
                elif self._tokens[i].value in ':,':
                    put_to_dict(self.operators, self._tokens[i].name)

                # Check whether there is an initialization
                if self._tokens[i].value in ':=':

                    # Skip until next delimiter
                    while not self._tokens[i].value in '=,;':
                        i += 1

                    # Exit loop if semicolon is found
                    if self._tokens[i].value == ';':
                        break
                    
                    if self._tokens[i].value == '=':
                        put_to_dict(self.operands, identifier.name)
                        put_to_dict(self.operators, self._tokens[i].name)
                        i += 1
                        
                        # Parse RValue
                        while not self._tokens[i].value in ';,':

                            # Parse function statement
                            if self._tokens[i].value == 'function':
                                i = self._parse_function_expression(i)
                                continue

                            # Put token to vocabulary
                            if self._tokens[i].is_operand:
                                put_to_dict(self.operands, self._tokens[i].name)
                            elif self._tokens[i].is_operator:
                                put_to_dict(self.operators, self._tokens[i].name)
                            i += 1
                        i -= 1 # To start outer loop with the last token
                i += 1
            
            # Put semicolon to dictionary
            put_to_dict(self.operators, self._tokens[i].name)

            # Return next token after ;
            return i + 1 