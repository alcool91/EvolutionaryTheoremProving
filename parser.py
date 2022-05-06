"""
build a parser for propositional logic
using the production rules defined in lecture slides
"""

from rply import ParserGenerator

from lexer import build_lexer
from ast_nodes import *

class ParseError(Exception): pass
class LexError(Exception): pass

def build_parser(tokens):
  pg = ParserGenerator(tokens)

  @pg.error
  def error_handler(token):
    raise ParseError(f'{token} at position {token.source_pos} is unexpected')

  @pg.production('wff : imp')
  @pg.production('wff : neg')
  def wff(p): return p[0]

  @pg.production('wff : WFF')
  def base_wff(p): return Wff(p[0].value)

  @pg.production('neg : OPAREN NOT wff CPAREN')
  def negate(p): return Negate(wff=p[2])

  @pg.production('imp : OPAREN wff IMPLIES wff CPAREN')
  def implies(p): return Implies(left=p[1], right=p[3])

  return pg.build()

# given a propositional formula f, parse the formula accordingly
def parse_proof(f):
  lexer = build_lexer()
  possible_tokens = [rule.name for rule in lexer.rules]
  parser = build_parser(possible_tokens)
  tokens = list(lexer.lex(f))
  return parser.parse(iter(tokens))
