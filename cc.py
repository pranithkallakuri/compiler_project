# -*- coding: utf-8 -*-
"""CC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xMGH4u-a2SDMlkQi-IWdbAhYnFgJ9heF
"""

# Whitespace and comment removal class
class CleanCode:

  commentFlag = 0

  def whiteSpaceRemover(self,line):
    while line[0] == ' ':                                                       # delete spaces before the line
      line = line[1:]
    while line[-1] == ' ':                                                      # delete spaces after the line
      line = line[:-1]
    preline = ''
    while preline != line :                                                     # cancel extra spaces by making two spaces as one until there are not more than one space at a place
     preline = line
     line = line.replace('  ',' ')
    return line

  def commentRemover(self,line):
    for i in range(len(line)):
      if line[i:i+2] == '//':                                                   # if // encountered, delete every string from that line after the first encounter of //
        line = line[:i]
        break
    i=0
    while i < len(line):                                                        
      if line[i:i+2] == '/*' and self.commentFlag == 0:                         # when /* encountered turn comment flag to 1 which only gets to 0 when a */ is encountered.
        self.commentFlag = 1
      elif line[i:i+2] == '*/' and self.commentFlag == 1:
        self.commentFlag = 0
        line = line[0:i] + line[i+2:]
      elif self.commentFlag == 1:                                               # delete every character until the commentflag is 1.
        line = line[0:i] + line[i+1:]
      else:
        i+=1
    return line

  def cleanCodeLine(self,line):
    return self.commentRemover(self.whiteSpaceRemover(line))

# The Tokenizer Class
class Tokenizer:
  def tokenizer(self,line):
    #keywords = ['int', 'float', 'boolean', 'string', 'while', 'until', 'if', 'else', 'true', 'false']
    delimiters = ['{', '}', '(', ')', '[', ']', ';', ',']
    operators = ['+', '-', '*', '/', '%', '=', ':=', '==', '>', '<', '>=', '<=', '!=', '&&', '||', '!', '?', ':']
    markers = delimiters + operators
    i=0
    while i < len(line):
      if line[i:i+2] in markers:                                                # if a double symbol delim or operat is encountered, add a space before and after that.
        line = line[:i]+' '+line[i:i+2]+' '+line[i+2:]
        i+=2
      elif line[i] in markers:                                                  # if a double symbol delim is not encountered, and a single symbol delim is encountered,
        line = line[:i]+' '+line[i:i+1]+' '+line[i+1:]                          # add a space before and after symbol
        i+=1
      i+=1
    return line.split()                                                         # split the line to list of tokens based on spaces.

# Driver Code    
clean = CleanCode()
token = Tokenizer()
print(token.tokenizer(clean.cleanCodeLine('hi hello //  uppal bal tiktok')))
print()
print(token.tokenizer(clean.cleanCodeLine('    for    get         (int i = = 0; i<&& n; i +/+)         ')))
print()
print(token.tokenizer(clean.cleanCodeLine('/* get the   fuk     out*/      of       here')))
print()
print(token.tokenizer(clean.cleanCodeLine('/* comment  */      int  ')))
print()
print(token.tokenizer(clean.cleanCodeLine('   i   =  0;')))
