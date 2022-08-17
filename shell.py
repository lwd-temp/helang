from helang.lexer import Lexer
from helang.parser import Parser
from helang.exceptions import BadStatementException, BadTokenException


def shell():
    env = dict()
    while True:
        text = input('Speak to Saint He > ').strip()
        if not text.endswith(';'):
            text += ';'
        lexer = Lexer(text)
        parser = Parser(lexer.lex())
        try:
            parser.parse().evaluate(env)
        except (BadStatementException, BadTokenException) as e:
            print(e)
        except:
            print('Error! Revise Saint He\'s videos!')


if __name__ == '__main__':
    shell()
