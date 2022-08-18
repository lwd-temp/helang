import sys
import threading

from ..lexer import Lexer
from ..parser import Parser
from ..exceptions import HeLangException
from typing import TextIO


class Runner(threading.Thread):
    def __init__(self, code: str, stdout: TextIO, stderr: TextIO):
        super().__init__()
        self.code = code
        self.stdout = stdout
        self.stderr = stderr

    def run(self):
        raw_stdout = sys.stdout
        raw_stderr = sys.stderr

        sys.stdout = self.stdout
        sys.stderr = self.stderr

        try:
            Parser(Lexer(self.code).lex()).parse().evaluate(dict())
        except HeLangException as e:
            print(f'{type(e).__name__}: {e}', file=sys.stderr)

        sys.stdout = raw_stdout
        sys.stderr = raw_stderr
