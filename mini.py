# ===============================================================================
# IMPORTS
# ===============================================================================

from error import *
from position import *
from constants import *
from lexer import *
from parser import *
import string
import os
import math


# ===============================================================================
# ERRORS
# ===============================================================================




# ===============================================================================
# NODES
# ===============================================================================





# ===============================================================================
# INTERMEDIATE CODE GENERATOR
# ===============================================================================
class IntermediateCodeGenerator:
    def __init__(self, ast):
        self.temp_counter = 0
        self.ast = ast

    def get_next_temp_var(self):
        self.temp_counter += 1
        return self.temp_counter - 1

    def get_current_temp(self):
        return self.temp_counter - 1

    def generate_intermediate_code(self):
        if self.ast == None:
            return ''
        return self.ast.get_ic(self.get_next_temp_var, self.get_current_temp)


# ===============================================================================
# RUN
# ===============================================================================


def run_lexer(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error


def run_parser(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error


def run_intermediate_code_generator(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Generate Intermediate Code
    icg = IntermediateCodeGenerator(ast.node)

    return icg.generate_intermediate_code(), ast.error


# TODO: Fix FOR and IF statements in the ICG
