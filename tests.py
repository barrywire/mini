import unittest
from basic import Lexer, Parser


class TestParser(unittest.TestCase):

    def test_parse_single_operation(self):
        lexer = Lexer("", "5 + 3")
        tokens, error = lexer.make_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(str(ast), "(5 + 3)")

    def test_parse_multiple_operations(self):
        lexer = Lexer("", "5 + 3 * 2")
        tokens, error = lexer.make_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(str(ast), "(5 + (3 * 2))")

    def test_parse_precedence(self):
        lexer = Lexer("", "5 + 3 * 2 / 4 - 1")
        tokens, error = lexer.make_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertEqual(str(ast), "((5 + ((3 * 2) / 4)) - 1)")


if __name__ == '__main__':
    unittest.main()
