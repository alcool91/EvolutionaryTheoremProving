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

  @pg.production('prover : newline? premises PROVES thm NEWLINE stmts')
  def prover(p): return Prover(premises=p[1], thm=p[3], stmts=p[-1])

  @pg.production('premises : OCURLY wffs CCURLY')
  def premises(p): return p[1]

  @pg.production('stmts : stmt NEWLINE stmts')
  def stmts(p): return [p[0]] + p[2]

  @pg.production('stmts : ')
  def stmts_empty(p): return []

  @pg.production('stmt : wff rule')
  def stmt(p): return p[0]

  @pg.production('stmt : wff binary_op wff rule')
  def stmt_nice(p): return Operator(name=p[1], operands=[p[0], p[2]], arity=2)

  @pg.production('thm : wff')
  def thm(p): return p[0]

  @pg.production('thm : wff binary_op wff')
  def thm_nice(p): return [Operator(name=p[1], operands=[p[0], p[2]], arity=2)]

  @pg.production('rule : ')
  def rule(p): pass

  @pg.production('wffs : wff COMMA wffs')
  def wffs(p): return [p[0]] + p[-1]

  @pg.production('wffs : ')
  def wffs_empty(p): return []

  # recursively define a well formed formula
  @pg.production('wff : OPAREN unary_op wff CPAREN')
  def wff_unary(p): return Operator(name=p[1], operands=[p[2]], arity=1)

  @pg.production('wff : OPAREN wff binary_op wff CPAREN')
  def wff_binary(p): return Operator(name=p[2], operands=[p[1], p[3]], arity=2)

  @pg.production('wff : ATOM') # <- base case
  def wff_atom(p): return p[0].value

  # helper production rules
  @pg.production('unary_op : NOT unary_op')
  def unary_op(p): return p[0].name

  @pg.production('unary_op : ')
  def unary_op_empty(p): pass

  @pg.production('binary_op : AND')
  @pg.production('binary_op : OR')
  @pg.production('binary_op : IMPLIES')
  @pg.production('binary_op : EQUIV')
  def binary_op(p): return p[0].value

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
  return parser.parse(iter(tokens))
