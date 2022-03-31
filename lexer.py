import re
from rply import LexerGenerator

# builds a lexer generator using the language of propositional logic
# matches against tokens using ...
def build_lexer():
  lg = LexerGenerator()

  # ignore comments
  lg.ignore(r'#.*')
  lg.ignore(r'[ \t]+')

  # handle whitespace
  lg.add('NEWLINE', r'\r|\n|(\n\r)|,')
  lg.ignore(r'[ \t]+')

  # unary connective
  lg.add('NOT', r'!')

  # binary connectives
  lg.add('AND', r'&')
  lg.add('OR', r'\|')
  lg.add('IMPLIES', r'=>')
  lg.add('EQUIV', r'<=>')

  # punctuation symbols
  lg.add('OPAREN', r'\(')
  lg.add('CPAREN', r'\)')

  # atomic propositional symbols
  lg.add('ATOM', r'[a-z]')

  return lg.build()