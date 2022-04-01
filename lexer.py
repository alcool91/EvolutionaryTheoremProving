import re
from rply import LexerGenerator

# builds a lexer for the language of propositional logic
# matches against tokens using syntax defined in lecture slides
def build_lexer():
  lg = LexerGenerator()

  # ignore comments
  lg.ignore(r'#.*')
  lg.ignore(r'[ \t]+')

  # handle whitespace
  lg.add('NEWLINE', r'\r|\n|(\n\r)|,')
  lg.add('COMMA', r'\,')
  lg.ignore(r'[ \t]+')

  # unary connective
  lg.add('NOT', r'!')

  lg.add('PROVES', r'\|=H')

  # binary connectives
  lg.add('AND', r'&')
  lg.add('OR', r'\|')
  lg.add('IMPLIES', r'=>')
  lg.add('EQUIV', r'<=>')

  # punctuation symbols
  lg.add('OPAREN', r'\(')
  lg.add('CPAREN', r'\)')
  lg.add('OCURLY', r'\{')
  lg.add('CCURLY', r'\}')

  # atomic propositional symbols
  lg.add('ATOM', r'[a-z]')

  return lg.build()