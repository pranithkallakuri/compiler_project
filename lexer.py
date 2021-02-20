# TEAM MEMBERS                   - G69
# PRANITH S KALLAKURI            - 2018A7PS0249H
# DANTULURI SAIRAJU              - 2018A7PS0306H
# GOLLA SAI VENKAT GOWTHAM       - 2018A7PS0991H
# NITIN GOPALA KRISHNA SONTINENI - 2018A7PS0262H


import sys                                # This import is required to use commandline argument for filename to be lexed. 
from tokenizer import Tokenizer, Token    # Importing the Tokenizer class custom written by us (the team)

# Checking if file to lex is provided as a commandline argument
if len(sys.argv) < 2:
    print("Please enter filename as commandline argument")
    print("Exiting...")
    exit()

# Creating an instance of a new Tokenizer Class that contains the lexer.
my_tokenizer = Tokenizer(sys.argv[1])

print()

while True:
    # Getting next token from input file until we hit EOF
    token = my_tokenizer.get_next_token()
    if token.token == "EOF":
        break

    #########################################################################################################
    # If error in Token, it is printed on the standard output stream. 
    # We identify 4 different classes of errors
    #     -invalid chars in string literals =================================================>> "string_error"
    #     -invalid char found in input stream ===============================================>> "char_error"
    #     -invalid floating point notation ==================================================>> "float_error"
    #     -miscellaneous errors (mostly detects only string tokens with missing closing ") ==>> "Invalid_Token"
    #########################################################################################################

    if token.token == "string_error" or token.token=="char_error" or token.token=="float_error" or token.token == "Invalid_Token" :
        print("Error encountered at line " + str(token.line))
    # Printing received token to output stream
    print("< " + token.token + ", " + token.lexeme + " >  b/w indices " + str(token.begin) + " to " + str(token.end) + " on line number " + str(token.line) + "\n")