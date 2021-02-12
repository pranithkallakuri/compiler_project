# Whitespace and comment removal class
class CleanCode:

  commentFlag = 0

  def whiteSpaceRemover(self,line):
    if len(line)==0:
      return ''
    while line[0] == ' ':                                                       # delete spaces before the line
      line = line[1:]
    while line[-1] == ' ':                                                      # delete spaces after the line
      line = line[:-1]
    preline = ''
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
    temp = [ r'{}'.format(line[i]) for i in range(len(line)) ]
    for i in range(len(temp)-1):
      if temp[i]=='\\' and temp[i+1]=='"':
        temp[i] = '@'
        temp[i+1] = '@'
      elif temp[i]=='\\':
        temp[i]='~'
    s1 = ''
    return self.whiteSpaceRemover(self.commentRemover(s1.join(temp)))

# The Tokenizer Class
class Tokenizer:
  def splitter(self,line):
    Tokens = []
    temp = ''
    stringflag = 0
    tokenflag = 1
    for i in range(len(line)):
      if line[i] == ' ' and stringflag == 0 and tokenflag==1:
        tokenflag = 0
      if line[i] != ' ':
        tokenflag = 1
      if line[i] == '"' and stringflag == 0:
        stringflag = 1
      elif line[i] == '"' and stringflag == 1:
        stringflag = 0
      if tokenflag == 1:
        temp+=line[i]
      elif tokenflag == 0 and temp!='':
        Tokens.append(temp)
        temp=''
      if i == len(line)-1:
        Tokens.append(temp)
      if '' in Tokens:
        Tokens.remove('')
      for i in range(len(Tokens)):
        Tokens[i] = Tokens[i].replace('@@','~"')
    return Tokens

  def tokenizer(self,line):
    #keywords = ['int', 'float', 'boolean', 'string', 'while', 'until', 'if', 'else', 'true', 'false']
    delimiters = ['{', '}', '(', ')', '[', ']', ';', ',']
    operators = ['+', '-', '*', '/', '%', '=', ':=', '==', '>', '<', '>=', '<=', '!=', '&&', '||', '!', '?', ':']
    markers = delimiters + operators
    stringflag = 0
    i=0
    while i < len(line):
      if line[i] == '"':
        stringflag = (stringflag+1)%2
      if line[i:i+2] in markers and stringflag==0:                                                # if a double symbol delim or operat is encountered, add a space before and after that.
        line = line[:i]+' '+line[i:i+2]+' '+line[i+2:]
        i+=2
      elif line[i] in markers and stringflag==0:                                                  # if a double symbol delim is not encountered, and a single symbol delim is encountered,
        line = line[:i]+' '+line[i:i+1]+' '+line[i+1:]                          # add a space before and after symbol
        i+=1
      i+=1
    return self.splitter(line)                                                       # split the line to list of tokens based on spaces.                                                               

# Driver Code    
clean = CleanCode()
token = Tokenizer()
print(token.tokenizer(clean.cleanCodeLine('hi hello //  uppal bal tiktok')))
print()
print(token.tokenizer(clean.cleanCodeLine(r'    for    get         (int i = = 0; i<&& n; i +/+)         ')))
print()
print(token.tokenizer(clean.cleanCodeLine(r'/* get the   fuk     out      of       here')))
print()
print(token.tokenizer(clean.cleanCodeLine(r' comment  */      int  ')))
print()
print(token.tokenizer(clean.cleanCodeLine(r' printf  ( " Hello World   \n) '))) #String doesn't work Its splitting 
print()
print(token.tokenizer(clean.cleanCodeLine(r'print(" hello \" world \\ raju\n pranith \t nitin") '))) #String doesn't work Its splitting 
print()
