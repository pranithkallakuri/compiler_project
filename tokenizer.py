# TEAM MEMBERS                   - G69
# PRANITH S KALLAKURI            - 2018A7PS0249H
# DANTULURI SAIRAJU              - 2018A7PS0306H
# GOLLA SAI VENKAT GOWTHAM       - 2018A7PS0991H
# NITIN GOPALA KRISHNA SONTINENI - 2018A7PS0262H


# Wrapper class for an identified token 
class Token:
    token = ""                                                # Contains the TK_identifier
    lexeme = ""                                               # Contains the actual lexeme
    begin = 0                                                 # Contains the start index of lexeme 
    end = 0                                                   # Contains end index of lexeme
    line = 0                                                  # Contains line number of lexeme
    def __init__(self, token_type, lexeme, begin, end, line):
        self.token = token_type
        self.lexeme = lexeme
        self.begin = begin
        self.end = end
        self.line = line

class Tokenizer:
    in_singleline_comment = False                          # Bool that keeps track whether currently pointer is in single line comment
    in_multiline_comment = False                           # Keeps track whether pointer in multiline comment
    state = "start"                                        # Keeps track of DFA state
    previous_final_state = "start"                         # Keeps track of previously found valid Token
    lb = 0                                                 # lb -> lexeme beginning pointer
    fp = 0                                                 # fp -> forward pointer 
    
    # List of keywords, operators and delimiters to which we match
    keywords = ['int', 'float', 'boolean', 'string', 'while', 'until', 'if', 'else', 'true', 'false', 'print']
    operators = ['+', '-', '*', '/', '%', ':=', '=', '==', '>', '<', '>=', '<=', '!=', '&&', '||', '!', '?', ':']
    delimiters = ['{', '}', '(', ')', '[', ']', ';', ',']
    delimiter_token = {
        '{' : "delim_leftcurlybrace",
        '}' : "delim_rightcurlybrace",
        '(' : "delim_leftparathesis",
        ')' : "delim_rightparanthesis",
        '[' : "delim_leftsquarebrace",
        ']' : "delim_rightsquarebrace",
        ';' : "delim_semicolon",
        ',' : "delim_comma"
    }
    token_list = []
    filename = ""
    error_state =""
    string_flag=0


    def __init__(self, filename):
        self.filename = filename
        self.get_token_list(self.filename)

    def get_next_token(self):                                       # Returns next token from the token-list
        if len(self.token_list) == 0:
            return Token("EOF", "EOF", -1, -1, -1)
        tok = self.token_list[0]
        self.token_list.pop(0)
        return tok

    def get_token_list(self, filename):
        file = open(filename, 'r')
        line_number = 1
        # Take each line of file in a buffer
        for line in file:
            ascii_list = [ord(line[i]) for i in range(len(line))]
            if ascii_list[-1] == 10:
                ascii_list.pop()
            # print()
            # print(ascii_list)
            # print(line)
            # print()
            self.state = "start"                                   # Reset start state to "start" at the beginning of each line buffer                                
            self.get_tokens(ascii_list, line_number)
            line_number += 1
            if self.in_singleline_comment:
                self.in_singleline_comment = False                 # Moving to next line if current is singleline comment
            #break
    
    def get_tokens(self, chars, line_number):
        self.lb = 0
        self.fp = 0
        is_final_state = False       
        while self.fp < len(chars):
            self.string_flag = 0
            if not self.in_multiline_comment:
                self.state, is_final_state = self.change_state(chars[self.fp], chars)
            # print(self.lb, self.fp, chr(chars[self.fp])) ##
            # print(self.state, is_final_state)
            # print("singlecomm = " + str(self.in_singleline_comment) + " " + "multicomm=" + str(self.in_multiline_comment))
            if self.in_multiline_comment:
                q = self.is_completely_multiline_comment(chars)        # Handling Multiline comment
                # print(q)
                if q:
                    return
                else:
                    continue
            if self.in_singleline_comment:                             # Skip current line iteration if in single-line comment
                return
            if self.state == "Error":                                  # Store Error Token
                lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp+1)))
                self.token_list.append(Token(self.error_state, lexeme_, self.lb, self.fp, line_number))
                self.previous_final_state = self.state
                is_final_state = False
                if self.string_flag == 1:
                    self.state = "str0"
                else:
                    self.state = "start"
                self.lb = self.fp+1

            if is_final_state and not self.in_multiline_comment:       # Store the successfully found lexeme
                lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp+1)))
                self.token_list.append(Token(self.state, lexeme_, self.lb, self.fp, line_number))
                self.previous_final_state = self.state
                is_final_state = False
                self.state = "start"
                self.lb = self.fp+1
            self.fp += 1
                

        if not self.in_multiline_comment and self.lb != self.fp:       # If line ends in incomplete lexeme, throw "Invalid_Error" Error and store
            # print("Error")
            lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp)))
            self.token_list.append(Token("Invalid_Token", lexeme_, self.lb, self.fp, line_number))

    def is_completely_multiline_comment(self, chars):                 # Iterate fp until end of multiline comment
        while self.fp < len(chars):
            if chars[self.fp] == ord('*'):
                self.fp += 1
                # print("are you failing multi")
                if self.fp < len(chars) and chars[self.fp] == ord('/'):
                    self.fp = self.fp+1 
                    self.lb = self.fp
                    # print("Changing multiline")
                    self.in_multiline_comment = False
                    return False
                else:
                    continue
            self.fp += 1
        return True


    def change_state(self, char, chars):                               # Method that changes the current state in DFA
        is_final_state = False
        if self.state == "start":                                      # If current state of DFA is "start"
            self.error_state = "char_error"
            # print("inhere1")                                         # Below are multiple possible state changes
            if char == ord('\n') or char == ord('\t') or char == ord(' '):
                self.lb = self.fp+1
                return self.state, is_final_state
            elif char == ord('/'):
                self.state = "ocom0"
                return self.state, is_final_state
            elif char == ord('='):
                self.state = "eq0"
                return self.state, is_final_state
            elif char == ord(':'):
                self.state = "col0"
                return self.state, is_final_state
            elif char == ord('<'):
                self.state = "lt0"
                return self.state, is_final_state
            elif char == ord('!'):
                self.state = "not0"
                return self.state, is_final_state
            elif char == ord('>'):
                self.state = "gt0"
                return self.state, is_final_state
            elif char == ord('&'):
                self.state = "and0"
                return self.state, is_final_state
            elif char == ord('|'):
                self.state = "or0"
                return self.state, is_final_state
            elif char == ord('+') or char == ord('-'):
                #print((self.fp+1 < len(chars)) and ((chars[self.fp+1]-48) not in range(1, 10)))
                if self.previous_final_state in ["integer_literal", "float_literal", "id", "string_literal"]:
                    self.state = "op_add" if char == ord('+') else "op_sub"
                    is_final_state = True
                    return self.state, is_final_state
                elif (self.fp+1 < len(chars)) and ((chars[self.fp+1]-48) not in range(1, 10)):
                    if (self.fp+2 < len(chars)) and chars[self.fp+1] == ord('0') and chars[self.fp+2] == ord('.'):
                        self.state = "int0"
                        return self.state, False
                    else:
                        self.state = "op_add" if char == ord('+') else "op_sub"
                        is_final_state = True
                        return self.state, is_final_state
                else:
                    self.state = "int0"
                    return self.state, is_final_state
            elif char == ord('*'):
                self.state = "op_mul"
                is_final_state = True
                return self.state, is_final_state
            elif char == ord('%'):
                self.state = "op_modulus"
                is_final_state = True
                return self.state, is_final_state
            elif char == ord('?'):
                self.state = "op_question"
                is_final_state = True
                return self.state, is_final_state
            elif chr(char).isalpha():
                self.state = "id"
                if self.fp+1 < len(chars) and (chr(chars[self.fp+1]).isalnum() or chars[self.fp+1] == ord('_')):
                    return self.state, is_final_state
                else:
                    is_final_state = True
                    if self.state in self.keywords:
                        self.state = "keyword"
                        return self.state, is_final_state
                    return self.state, is_final_state
            elif char == ord('"'):
                self.state = "str0"
                return self.state, is_final_state
            elif char == ord('0'):
                self.state = "intf0"
                if not (self.fp+1 < len(chars) and chars[self.fp+1] == ord('.')):
                    is_final_state = True
                    self.state = "integer_literal"
                    return self.state, is_final_state
                else:
                    return self.state, is_final_state
            elif chr(char).isdigit() and char != ord('0'):
                self.state = "intf1"
                if self.fp+1 < len(chars) and (chr(chars[self.fp+1]).isdigit() or chars[self.fp+1] == ord('.')):
                        return self.state, is_final_state
                else:
                    is_final_state = True
                    self.state = "integer_literal"
                    return self.state, is_final_state
            elif chr(char) in self.delimiters:
                self.state = self.delimiter_token[chr(char)]
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "id":                                          # If current state of DFA is "id"
            # print("inhere1.1", chr(char), char)
            if chr(char).isalnum() or char == ord('_'):
                if self.fp+1 < len(chars) and (chr(chars[self.fp+1]).isalnum() or chars[self.fp+1] == ord('_')):
                    return self.state, is_final_state
                else:
                    is_final_state = True
                    incomplete_lexeme = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp+1)))
                    # print(incomplete_lexeme)
                    if incomplete_lexeme in self.keywords:
                        # print("what about here?")
                        self.state = "keyword"
                        return self.state, is_final_state
                    return self.state, is_final_state

        elif self.state == "intf0":                                       # If current state of DFA is "intf0"
            # print("inhere1.2")
            if char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state

        elif self.state == "intf1":                                       # If current state of DFA is "intf1"
            # print("inhere1.3")
            if chr(char).isdigit():
                if self.fp+1 < len(chars) and (chr(chars[self.fp+1]).isdigit() or chars[self.fp+1] == ord('.')):
                        return self.state, is_final_state
                else:
                    is_final_state = True
                    self.state = "integer_literal"
                    return self.state, is_final_state
            elif char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state

        elif self.state == "str0":                                        # If current state of DFA is "str0"
            # print("inhere2")
            if char == ord('\\'):
                self.state = "str1"
                return self.state, is_final_state
            elif char == ord('"'):
                self.state = "string_literal"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.state = "str2"
                return self.state, is_final_state

        elif self.state == "str1":                                        # If current state of DFA is "str1"
            # print("inhere3")
            if chr(char) in ['"', '\\', 'n', 'r', 't']:
                self.state = "str2"
                return self.state, is_final_state
            else:
                self.error_state = "string_error"
                self.string_flag=1

        elif self.state == "str2":
            # print("inhere4")
            if char == ord('"'):
                self.state = "string_literal"
                is_final_state = True
                return self.state, is_final_state
            elif char == ord('\\'):
                self.state = "str1"
                return self.state, is_final_state
            else:
                return self.state, is_final_state
        
        elif self.state == "int0":                                     # If current state of DFA is "int0"
            # print("inhere5")
            # print("char = " + str(chr(char)))
            if chr(char).isdigit() and not char == ord('0'):
                # print("inhere5->1")
                self.state = "intf1"
                if self.fp+1 < len(chars) and chr(chars[self.fp+1]).isdigit():
                    return self.state, is_final_state
                else:
                    # print(chars[self.fp+1] == ord('.'))
                    if chars[self.fp+1] == ord('.'):
                        return self.state, is_final_state
                    else:
                        self.state = "integer_literal"
                        is_final_state = True
                        return self.state, is_final_state
            elif char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state
            elif char == ord('0'):
                self.state = "int1"
                return self.state, is_final_state
            else:
                self.retract()
                return "Error", False

        elif self.state == "int1":                                     # If current state of DFA is "int1"
            # print("inhere6")
            if char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state

        elif self.state == "float0":                                   # If current state of DFA is "float0"
            # print("inhere6")
            if chr(char).isdigit():
                self.state = "float_literal"
                if self.fp+1 < len(chars) and chr(chars[self.fp+1]).isdigit():
                    return self.state, is_final_state
                else:
                    is_final_state = True
                    return self.state, is_final_state
            else:
                self.error_state = "float_error"

        elif self.state == "float_literal":                            # If current state of DFA is "float_literal"
            # print("inhere6.1")
            if chr(char).isdigit():
                if self.fp+1 < len(chars) and chr(chars[self.fp+1]).isdigit():
                    return self.state, is_final_state
                else:
                    is_final_state = True
                    return self.state, is_final_state

        elif self.state == "ocom0":                                    # If current state of DFA is "ocom0"
            # print("inhere7")
            if char == ord('*'):
                self.state = "multilinecommentopen"
                self.in_multiline_comment = True
                is_final_state = True
                return self.state, is_final_state
            elif char == ord('/'):
                self.state = "singlelinecomment" 
                self.in_singleline_comment = True
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "op_div"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "eq0":                                      # If current state of DFA is "eq0"
            # print("inhere8")
            if char == ord('='):
                self.state = "relop_eq"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "op_assign"
                is_final_state = True
                return self.state, is_final_state
        
        elif self.state == "col0":                                     # If current state of DFA is "col0"
            # print("inhere9")
            if char == ord('='):
                self.state = "op_assign2"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "op_colon"
                return self.state, is_final_state

        elif self.state == "lt0":                                      # If current state of DFA is "lt0"
            # print("inhere10")
            if char == ord('='):
                self.state = "relop_le"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "relop_lt"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "not0":                                      # If current state of DFA is "not0"
            # print("inhere11")
            if char == ord('='):
                self.state = "relop_ne"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "op_not"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "gt0":                                       # If current state of DFA is "gt0"
            # print("inhere12")
            if char == ord('='):
                self.state = "relop_ge"
                is_final_state = True
                return state, is_final_state
            else:
                self.retract()
                self.state = "relop_gt"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "and0":                                       # If current state of DFA is "and0"
            # print("inhere13")
            if char == ord('&'):
                self.state = "logical_and"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "or0":                                        # If current state of DFA is "or0"
            # print("inhere14")
            if char == ord('|'):
                self.state = "logical_or"
                is_final_state = True
                return self.state, is_final_state
        
        self.state = "Error"                                             # If none DFA in none of the above state,..
        return self.state, is_final_state                                # ...move to sink state which is an "Error"
                
    def retract(self):                                                   # Retract method that decrements (retracts)...
        self.fp -= 1                                                     # ...fp by one.

        