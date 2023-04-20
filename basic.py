######################################################################
# IMPORTS
######################################################################
import string
from strings_with_arrows import *

######################################################################
# CONSTANTS
######################################################################
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

######################################################################
# ERRORS
######################################################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f' File {self.pos_start.file_name}, line {self.pos_start.line + 1}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.file_text,
                               self.pos_start, self.pos_end)
        return result


# Lexer Errors
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character - Lexer', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character - Lexer', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax - Parser', details)


######################################################################
# POSITION - Keeps track of the line number, column number, and index
######################################################################
class Position:
    def __init__(self, index, line, col, file_name, file_text):
        self.index = index
        self.line = line
        self.col = col
        self.file_name = file_name
        self.file_text = file_text

    # Move to the next index and update line and column numbers if necessary

    # def advance(self, current_char=None):
    def advance(self, current_char=None):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.line = 1
            self.col = 0

        return self

    # Create a copy of the current position
    def copy(self):
        return Position(self.index, self.line, self.col, self.file_name, self.file_text)


######################################################################
# TOKENS
######################################################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_EQ = 'EQ'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_COMMA = 'COMMA'
TT_ARROW = 'ARROW'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'


KEYWORDS = [
    'VAR',
    'AND',
    'OR',
    'NOT',
    'IF',
    'THEN',
    'ELIF',
    'ELSE',
    'FOR',
    'TO',
    'STEP',
    'WHILE',
    'FUN',
    'THEN',
    'RETURN',
    'CONTINUE',
    'BREAK',
    'END',
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


######################################################################
# LEXER
######################################################################
class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == ';\n':
                tokens.append(Token(TT_NEWLINE))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            # To modify once parser is implemented
            elif self.current_char in KEYWORDS:
                tokens.append(self.make_keyword())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                # tokens.append(Token(TT_EQ))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)

            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()

        escape_character = False

        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            # while self.current_char != None and self.current_char != '"':
            if escape_character:
                string += escape_characters.get(self.current_char,
                                                self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        identifier_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            identifier_str += self.current_char
            self.advance()

        token_type = TT_KEYWORD if identifier_str in KEYWORDS else TT_IDENTIFIER
        return Token(token_type, identifier_str, pos_start, self.pos)

    def make_minus_or_arrow(self):
        token_type = TT_MINUS
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == '>':
            self.advance()
            token_type = TT_ARROW

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        token_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        token_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        token_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_keyword(self):
        keyword_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            keyword_str += self.current_char
            self.advance()

        return Token(TT_KEYWORD, keyword_str, pos_start, self.pos)

######################################################################
# NODES - Nodes that build the Abstract Syntax Tree
######################################################################


class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class VariableAccessNode:
    def __init__(self, variable_name_token):
        self.variable_name_token = variable_name_token

        self.pos_start = self.variable_name_token.pos_start
        self.pos_end = self.variable_name_token.pos_end

    def __repr__(self):
        return f'{self.variable_name_token}'


class VariableAssignmentNode:
    def __init__(self, variable_name_token, value_node):
        self.var_token = Token(TT_KEYWORD, 'VAR')

        self.variable_name_token = variable_name_token
        self.value_node = value_node

        self.pos_start = self.variable_name_token.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f'{self.variable_name_token} {TT_EQ} {self.value_node}'


class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(
            self.cases) - 1][0]).pos_end

    #     # TOKEN definitions for the representation method
        self.if_token = Token(TT_KEYWORD, 'IF')
        self.then_token = Token(TT_KEYWORD, 'THEN')
        self.else_token = Token(TT_KEYWORD, 'ELSE')
        self.elif_token = Token(TT_KEYWORD, 'ELIF')

    def __repr__(self):
        if self.else_case is not None:
            # Start with the IF keyword and its condition
            res = f"({self.if_token}, {self.cases[0][0]}) "

            # Add the THEN keyword and its statement
            res += f"({self.then_token}, {self.cases[0][1]}) "

            # Add all the ELIF keywords, their conditions, and their statements
            for case in self.cases[1:]:
                res += f"({self.elif_token}, {case[0]}) "
                res += f"({self.then_token}, {case[1]}) "

                # Add the ELSE keyword and its statement
                res += f"({self.else_token}, {self.else_case})"
        else:
            # Start with the IF keyword and its condition
            res = f"({self.if_token}, {self.cases[0][0]}) "

            # Add the THEN keyword and its statement
            res += f"({self.then_token}, {self.cases[0][1]}) "

            # Add all the ELIF keywords and their conditions
            for case in self.cases[1:]:
                res += f"({self.elif_token}, {case[0]}) "
        return res


class ForNode:
    def __init__(self, variable_name_token, start_value_node, end_value_node, step_value_node, body_node):
        self.variable_name_token = variable_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.variable_name_token.pos_start
        self.pos_end = self.body_node.pos_end

        # TOKEN definition for the representation method
        self.for_token = Token(TT_KEYWORD, 'FOR')
        self.to_token = Token(TT_KEYWORD, 'TO')
        self.then_token = Token(TT_KEYWORD, 'THEN')

    def __repr__(self):
        return f'{self.for_token} {self.variable_name_token} {TT_EQ} {self.start_value_node} {self.to_token} {self.end_value_node} {self.then_token} {self.step_value_node} {self.body_node}'


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

        # TOKEN implementation for the Representation method
        self.while_token = Token(TT_KEYWORD, 'WHILE')
        self.then_token = Token(TT_KEYWORD, 'THEN')

    def __repr__(self):
        return f'{self.while_token} {self.condition_node} {self.then_token} {self.body_node}'

######################################################################
# PARSER
######################################################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self, ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    # ====================================================================

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    # ====================================================================

    def atom(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        # There's an elif here for TT_IDENTIFIER, but it's not implemented yet.
        # This is to enable use of variables in arithmetic expressions.

        elif token.type in (TT_LPAREN):
            res.register_advancement()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))
        elif token.matches(TT_KEYWORD, 'IF'):
            if_expression = res.register(self.if_expression())
            if res.error:
                return res
            return res.success(if_expression)

        elif token.matches(TT_KEYWORD, 'FOR'):
            for_expression = res.register(self.for_expression())
            if res.error:
                return res
            return res.success(for_expression)

        elif token.matches(TT_KEYWORD, 'WHILE'):
            while_expression = res.register(self.while_expression())
            if res.error:
                return res
            return res.success(while_expression)

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected an integer, a float, an identifier, or '+', '-' or '('"
        ))

    # =============================================================================

    def if_expression(self):
        res = ParseResult()

        cases = []
        else_case = None

        if not self.current_token.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'IF'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        expression = res.register(self.expression())
        if res.error:
            return res
        cases.append((condition, expression))

        while self.current_token.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expression())

            if res.error:
                return res

            if not self.current_token.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'THEN'"
                ))

            res.register_advancement()
            self.advance()

            expression = res.register(self.expression())
            if res.error:
                return res
            cases.append((condition, expression))

        if self.current_token.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expression())
            if res.error:
                return res
        # MIGHT BE BUGGY
        elif self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'ELSE' or 'EOF'"
            ))

        return res.success(IfNode(cases, else_case))

    def for_expression(self):
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected an identifier"
            ))

        var_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expression())
        if res.error:
            return res

        if self.current_token.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expression())
            if res.error:
                return res

        else:
            step_value = None

        if not self.current_token.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expression())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expression(self):
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expression())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def power(self):
        return self.binary_operation(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        elif token.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VariableAccessNode(token))

        return self.power()

    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expression(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected identifier"
                ))

            variable_name = self.current_token
            res.register_advancement()
            self.advance()

            if self.current_token.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            expression = res.register(self.expression())
            if res.error:
                return res
            return res.success(VariableAssignmentNode(variable_name, expression))

        node = res.register(self.binary_operation(
            self.comparison_expression, ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'VAR', int, float, identifier, '+', '-', '(' or 'NOT'"
            ))

        # return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))
        return res.success(node)

    def binary_operation(self, func_a, operation_tokens, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_token.type in operation_tokens or (self.current_token.type, self.current_token.value) in operation_tokens:
            # token = self.current_token
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinaryOpNode(left, op_token, right)

        return res.success(left)

    def comparison_expression(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, 'NOT'):
            op_token = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comparison_expression())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_token, node))

        node = res.register(self.binary_operation(
            self.arithmetic_expression,  (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected an integer, a float, an identifier, or '+', '-', '('  or 'NOT'"
            ))

        return res.success(node)

    def arithmetic_expression(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))


################################# #####################################
# PARSE RESULT - To check if there is any errors
######################################################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register_advancement(self):
        pass

    # Used for parsing and parse results
    def register(self, res):
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


######################################################################
# SYMBOL TABLE - To store variables
######################################################################
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


######################################################################
# RUN
######################################################################

def run(file_name, text):
    # Generate tokens
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    # return tokens, error

    # Generate Abstract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
