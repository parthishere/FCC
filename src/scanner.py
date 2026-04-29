from .helper import Token, TokenType, KEYWORDS

class Scanner:
    def __init__(self, source, filepath):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 0
        self.start = 0
        self.has_error = False
        self.filename = filepath
        self.line_char_count = 0

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current;
            self.scanToken()

        self.addToken(TokenType.EOF, None)

    def scanToken(self):
        character = self.advance()
        match character:
            case '(':
                self.addToken(TokenType.OPEN_PAR, "(")
            case ')':
                self.addToken(TokenType.CLOSE_PAR, ")")
            case '{':
                self.addToken(TokenType.OPEN_BRACE, "{")
            case '}':
                self.addToken(TokenType.CLOSE_BRACE, "}")
            case ';':
                self.addToken(TokenType.SEMICOLON, ";")
            case ',':
                self.addToken(TokenType.COMMA, ",")
            case '/':
                if self.match('/'):
                    while self.peek() != '\n': 
                        self.advance()
                    self.addToken(TokenType.COMMENT, self.source[self.start+2:self.current])
                elif self.match('*'):
                    while self.peek() != '*':
                        if self.peek() == '\n':
                            self.line += 1
                        self.advance()

                    if self.advance(): # consume * 
                        self.line += 1

                    if self.peek() != '/':
                        self.error("Something went wrong")
                        return
                    
                    if self.advance(): # consume /
                        self.line += 1
                        
                    self.addToken(TokenType.MULTILINE_COMMENT, self.source[self.start+2:self.current])
                else:
                    self.addToken(TokenType.SLASH, "/")
                pass
            case '*':
                self.addToken(TokenType.STAR, "*")
            case '.':
                self.addToken(TokenType.DOT, ".")
            case '-':
                self.addToken(TokenType.MINUS, "-")
            case '+':
                self.addToken(TokenType.PLUS, "+")

            case '!':
                if self.match('='):
                    self.addToken(TokenType.BANG_EQUAL, "!=")
                else:
                    self.addToken(TokenType.BANG, "!")
            case '=':
                if self.match('='):
                    self.addToken(TokenType.EQUAL_EQUAL, "==")
                else:
                    self.addToken(TokenType.EQUAL, "=")
            case '>':
                if self.match('='):
                    self.addToken(TokenType.GREATER_EQUAL, ">=")
                else:
                    self.addToken(TokenType.GREATER, ">")
            case '<':
                if self.match('='):
                    self.addToken(TokenType.LESS_EQUAL, "<=")
                else:
                    self.addToken(TokenType.LESS, "<")
            
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1
                self.line_char_count = 0

            case '"':
                self.string()

            case _:
                if self.isDigit(character):
                    self.digit()
                elif self.isAlpha(character):
                    self.identifier()
                else:
                    self.error("Unexpected Char")

    def error(self, string:str):
        print(f"\n! Token Error: \n{self.filename}:{self.line+1}:{self.line_char_count}")

        line_start = self.source.rfind('\n', 0, self.current) + 1
        line_end = self.source.find('\n', self.current)
        if line_end == -1:
            line_end = len(self.source)

        line = self.source[line_start:line_end]
        column = self.line_char_count - 1

        prefix = f"{self.line+1} | "
        error_string = f"{prefix}{line}\n{' ' * len(prefix)}{' ' * column}^"
        print(f"{error_string}\n")
        self.has_error = True
        
    def peek(self, char:str='', step:int=0):
        if self.isAtEnd(step=step):
            return None
        
        index = self.current + step;
        
        if char != '':
            return (char == self.source[index])
        else:
            return self.source[index]
    
    def match(self, char:str):
        if self.isAtEnd():
            return False
        elif self.source[self.current] != char:
            return False
        
        self.current += 1
        return True
    
    def advance(self, step:int=0):
        char = self.source[self.current]
        self.current += 1
        self.line_char_count += 1
        return char

    def isAtEnd(self, step:int=0):
        if (self.current + step) >= len(self.source):
            return True
        return False
    
    def addToken(self, type:TokenType, value=None, line:int=0, column:int=0):
        self.tokens.append(
            Token(type, value, self.line, self.line_char_count)
        )
        return self.tokens
    
    def isDigit(self, char:str):
        if not char:
            return None
        return (char >= '0' and char <= '9')
    
    def isAlpha(self, char:str):
        if not char:
            return None
        
        return ((char >= 'a' and char <= 'z') or 
                (char >= 'A' and char <= 'Z') or 
                (char == '_'))
    
    def isAlphaNumeric(self, char:str):
        return self.isDigit(char) or self.isAlpha(char)
    
    def string(self:str):
        while self.peek() != '"' and self.peek():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if not self.peek() or self.advance() != '"':
            self.error("Unterminated string")
            return

        string = self.source[self.start+1:self.current-1]
        self.addToken(type=TokenType.STRING, value=string, column=self.current-1)
        return string
    
    def digit(self):
        isFloat = False

        while self.isDigit(self.peek()):
            self.advance()

        if self.peek(".") and self.isDigit(self.peek(step=1)):
            isFloat = True
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
                
        if self.peek("."):
            self.error("Syntax error")
            return

        string = self.source[self.start:self.current]
        number = float(string) if isFloat else int(string)
        self.addToken(type=TokenType.CONSTANT, value=number)
        return number

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        
        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER) 
        self.addToken(token_type, value=text)
        return text
            

            