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

# Class for counting Holsted measures
class HolstedMeasures:
    def __init__(self, src):
        self._tokens = tokenize(src)
        self.operands = {}
        self.operators = {}
        self._parse_block(0)
        self._correct_operators()
        self._correct_operands()
        self._operands_total, self._operators_total = 0, 0

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
            
            # Take 2 identifiers and 1 : from dictionaries if there is a label
            if self._tokens[i].value in ['break', 'continue'] and self._tokens[i + 1].value != ';':
                take_from_dict(self.operands, self._tokens[i + 1].name, 2)
                take_from_dict(self.operators, ':')
            
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
    
    # Method to correct operators
    def _correct_operators(self):

        # Correct complex operators
        for key, counter in self.operators.copy().items():
            if key == '(...)':
                rm_from_dict(self.operators, ')')
            elif key == '[...]':
                rm_from_dict(self.operators, ']')
            elif key == '{...}':
                rm_from_dict(self.operators, '}')
            elif key == 'for/in(...)':
                take_from_dict(self.operators, '(...)', counter)
                take_from_dict(self.operators, 'in', counter)
            elif key in ['for(...;...;...)', 'while(...)', 'if(...)else']:
                take_from_dict(self.operators, '(...)', counter)
            elif key == '...?...:...':
                take_from_dict(self.operators, ':', counter)
            elif key == 'switch(...){...}':
                take_from_dict(self.operators, '(...)', counter)
                take_from_dict(self.operators, '{...}', counter)
            elif key in ['try/catch/finally', 'catch', 'finally']:
                take_from_dict(self.operators, '{...}', counter)
            elif key == 'do{...}while(...)':
                take_from_dict(self.operators, 'while(...)', counter)
                take_from_dict(self.operators, '{...}', counter)
            elif key[-5:] == '(...)':
                take_from_dict(self.operators, '(...)', counter)
            rm_from_dict(self.operators, 'catch')
            rm_from_dict(self.operators, 'finally')

        # Remove not existing operators
        for key, counter in self.operators.copy().items():
            if counter <= 0:
                del self.operators[key]
    
    # Method to correct operands
    def _correct_operands(self):

        # Remove not existing operands
        for key, counter in self.operands.copy().items():
            if counter <= 0:
                del self.operands[key]

    @property
    def operands_vocabulary(self):
        return len(self.operands)
    
    @property
    def operators_vocabulary(self):
        return len(self.operators)
    
    @property
    def operands_total(self):  
        if self._operands_total == 0:
            for key, occurence_count in self.operands.items():
                self._operands_total += occurence_count
        return self._operands_total
        
    @property
    def operators_total(self):   
        if self._operators_total == 0:
            for key, occurence_count in self.operators.items():
                self._operators_total += occurence_count
        return self._operators_total
        
    @property
    def program_vocabulary(self):
        return self.operands_vocabulary + self.operators_vocabulary
        
    @property
    def program_length(self):
        return self.operands_total + self.operators_total
        
    @property
    def program_volume(self):
        import math
        return math.ceil(self.program_length * math.log2(self.program_vocabulary))