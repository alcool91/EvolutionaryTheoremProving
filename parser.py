from rply import ParserGenerator

from lexer import build_lexer
from ast_nodes import *

class ParseError(Exception): pass
class LexError(Exception): pass

"""
build a parser for propositional logic
using the production rules defined in lecture slides
"""
def build_parser(tokens):
  pg = ParserGenerator(tokens)

  @pg.production('proof : newline? exprs+')
  def proof(p): return p[0]

  @pg.production('exprs+ : expr NEWLINE exprs*')
  def one_or_more_exprs(p): return [p[0]] + p[-1]

  @pg.production('exprs* : expr NEWLINE exprs*')
  def exprs(p): return [p[0]] + p[-1]

  @pg.production('exprs* : ')
  def exprs_empty(p): return []

  # recursively define an expression
  @pg.production('expr : OPAREN unary_expr CPAREN')
  @pg.production('expr : OPAREN binary_expr CPAREN')
  def expr(): pass

  @pg.production('expr : ATOM') # <- base case
  def expr_atom(p): return Atom(p[0].value)

  @pg.production('unary_expr : unary_op expr')
  def unary_expr(p): return UnaryExpr(name=p[0].value, children=p[1])

  @pg.production('binary_expr : OPAREN expr binary_op expr CPAREN')
  def binary_expr(p): return BinaryExpr(name=p[2], children=[p[1]] + p[3])

  # helper production rules
  @pg.production('unary_op : NOT')
  def unary_op(p): return p[0]

  @pg.production('binary_op : AND')
  @pg.production('binary_op : OR')
  @pg.production('binary_op : IMPLIES')
  @pg.production('binary_op : EQUIV')
  def binary_op(p): return p[0]

  @pg.production('newline? : NEWLINE')
  @pg.production('newline? : ')
  def newline(p): pass

  return pg.build()

# given a propositional formula f, parse the formula accordingly
def parse_proof(f):
  lexer = build_lexer()
  possible_tokens = [rule.name for rule in lexer.rules]
  parser = build_parser(possible_tokens)
  tokens = list(lexer.lex(f))
  print(tokens)
  return parser.parse(iter(tokens))
