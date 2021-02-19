# Python 3.8.5 64-bit

class Token:
    token = ""
    lexeme = ""
    begin = 0
    end = 0
    line = 0
    def __init__(self, token_type, lexeme, begin, end, line):
        self.token = token_type
        self.lexeme = lexeme
        self.begin = begin
        self.end = end
        self.line = line

class Tokenizer:
    in_singleline_comment = False
    in_multiline_comment = False
    state = "start"
    previous_final_state = "start"
    lb = 0
    fp = 0
    
    keywords = ['int', 'float', 'boolean', 'string', 'while', 'until', 'if', 'else', 'true', 'false']
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

    def get_next_token(self):
        if len(self.token_list) == 0:
            return Token("EOF", "EOF", -1, -1, -1)
        tok = self.token_list[0]
        self.token_list.pop(0)
        return tok

    def get_token_list(self, filename):
        file = open(filename, 'r')
        line_number = 1
        for line in file:
            ascii_list = [ord(line[i]) for i in range(len(line))]
            if ascii_list[-1] == 10:
                ascii_list.pop()
            # print()
            # print(ascii_list)
            # print(line)
            # print()
            self.state = "start"
            self.get_tokens(ascii_list, line_number)
            line_number += 1
            if self.in_singleline_comment:
                self.in_singleline_comment = False              # Moving to next line if current is singleline comment
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
                q = self.is_completely_multiline_comment(chars) 
                # print(q)                        # Handling Multiline comment
                if q:
                    return
                else:
                    continue
            if self.in_singleline_comment:
                return
            if self.state == "Error":
                lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp+1)))
                self.token_list.append(Token(self.error_state, lexeme_, self.lb, self.fp, line_number))
                self.previous_final_state = self.state
                is_final_state = False
                if self.string_flag == 1:
                    self.state = "str0"
                else:
                    self.state = "start"
                self.lb = self.fp+1

            if is_final_state and not self.in_multiline_comment:
                lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp+1)))
                self.token_list.append(Token(self.state, lexeme_, self.lb, self.fp, line_number))
                self.previous_final_state = self.state
                is_final_state = False
                self.state = "start"
                self.lb = self.fp+1
            self.fp += 1
                

        if not self.in_multiline_comment and self.lb != self.fp:
            # print("Error")
            lexeme_ = str(''.join(chr(chars[i]) for i in range(self.lb, self.fp)))
            self.token_list.append(Token("Invalid_Token", lexeme_, self.lb, self.fp, line_number))

    def is_completely_multiline_comment(self, chars):
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

    def change_state(self, char, chars):
        is_final_state = False
        if self.state == "start":
            self.error_state = "char_error"
            # print("inhere1")
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
                if self.previous_final_state in ["integer_literal", "float_literal", "id"]:
                    state = "op_add" if char == ord('+') else "op_sub"
                    is_final_state = True
                    return state, is_final_state
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

        elif self.state == "id":
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

        elif self.state == "intf0":
            # print("inhere1.2")
            if char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state

        elif self.state == "intf1":
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

        elif self.state == "str0":
            # print("inhere2")
            if char == ord('\\'):
                self.state = "str1"
                return self.state, is_final_state
            elif char == ord('"'):
                self.state == "string_literal"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.state = "str2"
                return self.state, is_final_state

        elif self.state == "str1":
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
        
        elif self.state == "int0":
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

        elif self.state == "int1":
            # print("inhere6")
            if char == ord('.'):
                self.state = "float0"
                return self.state, is_final_state

        elif self.state == "float0":
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

        elif self.state == "float_literal":
            # print("inhere6.1")
            if chr(char).isdigit():
                if self.fp+1 < len(chars) and chr(chars[self.fp+1]).isdigit():
                    return self.state, is_final_state
                else:
                    is_final_state = True
                    return self.state, is_final_state

        elif self.state == "ocom0":
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

        elif self.state == "eq0":
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
        
        elif self.state == "col0":
            # print("inhere9")
            if char == ord('='):
                self.state = "op_assign2"
                is_final_state = True
                return self.state, is_final_state
            else:
                self.retract()
                self.state = "op_colon"
                return self.state, is_final_state

        elif self.state == "lt0":
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

        elif self.state == "not0":
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

        elif self.state == "gt0":
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

        elif self.state == "and0":
            # print("inhere13")
            if char == ord('&'):
                self.state = "logical_and"
                is_final_state = True
                return self.state, is_final_state

        elif self.state == "or0":
            # print("inhere14")
            if char == ord('|'):
                self.state = "logical_or"
                is_final_state = True
                return self.state, is_final_state
        
        self.state = "Error"
        return self.state, is_final_state
                
    def retract(self):
        self.fp -= 1

        

# test_tokenizer = Tokenizer()
# my_token_list = test_tokenizer.get_token_list('sample.txt')
# print()
# print()
# print()
# for token in my_token_list:
#     print("< " + token.token + ", " + token.lexeme + " >")