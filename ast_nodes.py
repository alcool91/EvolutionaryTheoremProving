"""
ast nodes of a proof
"""

class Prover(): 
  """
  Represents a prover that is trying to prove a theorem
  """
  def __init__(self, premises, thm, stmts):
    self.premises = premises
    self.to_prove = thm
    self.stmts = stmts

  def __repr__(self):
    res = ''.join([repr(op) for op in self.premises]) if self.premises else ''
    res = '{' + res + '}'
    res += " |=H " + repr(self.to_prove)
    res += '\n' + ''.join([repr(stmt) for stmt in self.stmts])
    return res

class Operator():
  """
  Represents an operator on two different prop logic formulas
  """
  def __init__(self, name, operands, arity):
    self.name = name
    self.operands = operands
    self.arity = arity

  def __repr__(self):
    name = self.name
    if self.arity == 1:
      rep = repr(self.operands[0])
      return f"({name} {rep})"
    else:
      rep0 = repr(self.operands[0])
      rep1 = repr(self.operands[1])
      return f"({rep0} {name} {rep1})"