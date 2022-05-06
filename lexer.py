import re
from rply import LexerGenerator

# builds a lexer for the language of propositional logic
# matches against tokens using syntax defined in lecture slides
def build_lexer():
  lg = LexerGenerator()

  # handle whitespace
  lg.ignore(r'[ \t]+')

  # unary connective
  lg.add('NOT', r'!')
  lg.add('IMPLIES', r'=>')

  # punctuation symbols
  lg.add('OPAREN', r'\(')
  lg.add('CPAREN', r'\)')

  # atomic propositional symbols
  lg.add('WFF', r'[A-Z]')

  return lg.build()