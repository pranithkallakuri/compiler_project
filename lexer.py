#Python 3.9.1 64-bit

import sys      # This import is required to use commandline argument for filename to be lexed. 
from tokenizer import Tokenizer, Token

if len(sys.argv) < 2:
    print("Please enter filename as commandline argument")
    print("Exiting...")
    exit()


my_tokenizer = Tokenizer(sys.argv[1])

print()

while True:
    token = my_tokenizer.get_next_token()
    if token.token == "EOF":
        break
    if token.token == "string_error" or token.token=="char_error" or token.token=="float_error" or token.token == "Invalid_Token" :
        print("Error encountered at line " + str(token.line))
    print("< " + token.token + ", " + token.lexeme + " >  b/w indices " + str(token.begin) + " to " + str(token.end) + " on line number " + str(token.line))