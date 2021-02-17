#Python 3.8.5 64-bit
#Written by Pranith S Kallakuri

import sys      # This import is required to use commandline argument for filename to be lexed. 
from tokenizer import Tokenizer, Token

if len(sys.argv) < 2:
    print("Please enter filename as commandline argument")
    print("Exiting...")
    exit()


my_tokenizer = Tokenizer(sys.argv[1])

print()
print()
print()
print()

while True:
    token = my_tokenizer.get_next_token()
    if token.token == "EOF":
        break
    print("< " + token.token + ", " + token.lexeme + " >  b/w indices " + str(token.begin) + " to " + str(token.end) + " on line number " + str(token.line))