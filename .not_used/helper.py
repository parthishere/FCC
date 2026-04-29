
# TOKEN_PATTERNS = [
#     TokenPattern(TokenType.MULTILINE_COMMENT, r'^/\*[\s\S.]*?\*/'),
#     TokenPattern(TokenType.COMMENT, r'//.*'),

#     TokenPattern(TokenType.WHITESPACE, r'\s+'),
#     TokenPattern(TokenType.OPEN_PAR, r'\(', "("),
#     TokenPattern(TokenType.CLOSE_PAR, r'\)', ")"),
#     TokenPattern(TokenType.OPEN_BRACE, r'\{'),
#     TokenPattern(TokenType.CLOSE_BRACE, r'\}'),
#     TokenPattern(TokenType.SEMICOLON, r';'),
#     TokenPattern(TokenType.COMMA, r','),
#     TokenPattern(TokenType.SLASH, r'/'),
#     TokenPattern(TokenType.STAR, r'\*'),
#     TokenPattern(TokenType.DOT, r'\.'),
#     TokenPattern(TokenType.MINUS, r'-'),
#     TokenPattern(TokenType.PLUS, r'\+'),

#     TokenPattern(TokenType.BANG_EQUAL, r'!='),
#     TokenPattern(TokenType.EQUAL_EQUAL, r'=='),
#     TokenPattern(TokenType.GREATER_EQUAL, r'>='),
#     TokenPattern(TokenType.LESS_EQUAL, r'<='),
#     TokenPattern(TokenType.BANG, r'!'),
#     TokenPattern(TokenType.EQUAL, r'='),
#     TokenPattern(TokenType.GREATER, r'>'),
#     TokenPattern(TokenType.LESS, r'<'),

#     TokenPattern(TokenType.AND, r'\band\b'),
#     TokenPattern(TokenType.CLASS, r'\bclass\b'),
#     TokenPattern(TokenType.ELSE, r'\belse\b'),
#     TokenPattern(TokenType.FALSE, r'\bfalse\b'),
#     TokenPattern(TokenType.FUN, r'\bfun\b'),
#     TokenPattern(TokenType.FOR, r'\bfor\b'),
#     TokenPattern(TokenType.IF, r'\bif\b'),
#     TokenPattern(TokenType.NIL, r'\bnil\b'),
#     TokenPattern(TokenType.OR, r'\bor\b'),
#     TokenPattern(TokenType.PRINT, r'\bprint\b'),
#     TokenPattern(TokenType.RETURN, r'\breturn\b'),
#     TokenPattern(TokenType.SUPER, r'\bsuper\b'),
#     TokenPattern(TokenType.THIS, r'\bthis\b'),
#     TokenPattern(TokenType.TRUE, r'\btrue\b'),
#     TokenPattern(TokenType.VAR, r'\bvar\b'),
#     TokenPattern(TokenType.WHILE, r'\bwhile\b'),

#     TokenPattern(TokenType.STRING, r'"[^"]*"'),
#     TokenPattern(TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
#     TokenPattern(TokenType.CONSTANT, r'([0-9]+)(\.[0-9]+)?'),
# ]




# def tokenize(source):

#     # while index < len(source):
#     #     print(index, source[index])
#     #     index+=1
#     # print()
    
#     tokens = []
#     index = 0
#     line = 1
#     current_line_words = 0

#     try:
#         while index < len(source):
#             token_parsing = False
#             for token in TOKEN_PATTERNS:
#                 re_match = token.regex.match(source, index)

#                 if not re_match:
#                     continue

#                 value = re_match.group()
#                 if token.type == TokenType.WHITESPACE:
#                     if '\n' in value:
#                         current_line_words = 0
#                         line += value.count('\n')
#                 else:
#                     tokens.append(
#                         Token(token.type, f"{source[index:re_match.end()].strip()}", line, index
#                     ))
#                     current_line_words += re_match.end() - index
#                 index = re_match.end()
#                 break
#             if not re_match:
#                 raise LookupError(f"Token Error: \n{raw_filename_path}:{line}:{current_line_words}:  \n```{line} | {source[index:].split("\n")[0]}``` <--  \ntotal word parsed {index}");

#     except LookupError as e:
#         print(e)

#     finally:
#         print(tokens)
#         pass
        

# def assembler(retval):
#     assembly_format = f""".global _main
# _main:
#     mov	w0, #{retval}
#     ret"""

#     with open("temp.s", "w") as file:
#         file.write(assembly_format)