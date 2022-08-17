import sys
import traceback

from typing import Dict
from helang.lexer import Lexer
from helang.parser import Parser
from helang.exceptions import BadStatementException, BadTokenException, HeLangException
from helang.u8 import U8


SHELL_HELP = """
.help  Print this help message
.exit  Exit the shell
.env   Print current environments
""".strip()


def process_shell_keywords(text: str, env: Dict[str, U8]):
    if text == 'help':
        print(SHELL_HELP)
    elif text == 'exit':
        print('Saint He bless you.')
        sys.exit(0)
    elif text == 'env':
        for k, v in env.items():
            print(f'{k}: {v}')
    else:
        print(f'invalid shell keyword: {text}')


def shell():
    env = dict()
    while True:
        text = input('Speak to Saint He > ').strip()
        if text == '':
            continue

        if text.startswith('.'):
            process_shell_keywords(text[1:], env)
            continue

        if not text.endswith(';'):
            text += ';'
        lexer = Lexer(text)
        parser = Parser(lexer.lex())
        try:
            parser.parse().evaluate(env)
        except (BadTokenException, BadStatementException):
            traceback.print_exc()
        except HeLangException as e:
            print('Fatal Error! Revise Saint He\'s videos!')
            raise e


if __name__ == '__main__':
    shell()
