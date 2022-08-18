import sys
import threading

from ..lexer import Lexer
from ..parser import Parser
from typing import TextIO


class Runner(threading.Thread):
    def __init__(self, code: str, redirect_file: TextIO):
        super().__init__()
        self.code = code
        self.redirect_file = redirect_file

    def run(self):
        raw_stdout = sys.stdout
        sys.stdout = self.redirect_file
        Parser(Lexer(self.code).lex()).parse().evaluate(dict())
        sys.stdout = raw_stdout
