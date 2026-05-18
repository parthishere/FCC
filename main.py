import argparse
from src.scanner import Scanner
from src.parser import Paser
from src.helper import Token, TokenType
from src.interpreter import Interpret
from src.resolver import Resolver

raw_filename_path = ""
filename_ext = ""
filename = ""
extention = ""


def main(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # print(content)
            scanner = Scanner(content, file_path)
            scanner.scanTokens()
            # print(sc.tokens)
            if(scanner.has_error): 
                return

            parser = Paser(scanner.tokens, content, file_path)
            if(parser.has_error): 
                return

            statments = parser.parse()
            print(statments)
            parser.validate()

            interpreter = Interpret(statments, content, file_path)
            resolver = Resolver(interpreter)
            resolver.resolve(statments)

            interpreter.interpret()

    except Exception as e:
        print(e)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='FCC - Fuck C Compiler',
                    description='It compiles',
                    epilog='issue --help for more info')
    parser.add_argument('filename')
    parser.add_argument('-b', '--backend')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    raw_filename_path = args.filename
    filename_ext = args.filename.split("/")[-1]
    filename = filename_ext.split(".")[0]
    extention = filename_ext.split(".")[-1]

    main(raw_filename_path)
