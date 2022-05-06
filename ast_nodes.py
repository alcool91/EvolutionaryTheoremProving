import copy

class Negate:
  def __init__(self, wff):
    self.wff = wff

  def height(self):
    return wff.height() + 1

  def _clone(self): return copy.deepcopy(self)

  def __repr__(self): return '(!' + repr(self.wff) + ')'

  def __hash__(self):
    return hash(repr(self))

  def get_vars(self):
    return self.wff.get_vars()

class Implies:
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def height(self):
    return max(self.left.height(), self.right.height()) + 1

  def _clone(self): return copy.deepcopy(self)

  def __repr__(self): return '(' + repr(self.left) + ' => ' + repr(self.right) + ')'

  def __hash__(self):
    return hash(repr(self))

  def get_vars(self):
    return self.left.get_vars().union(self.right.get_vars())

class Wff:
  def __init__(self, symbol):
    self.symbol = symbol

  def _clone(self): return copy.deepcopy(self)

  def height(self): return 0

  def __repr__(self): return self.symbol

  def __hash__(self):
    return hash(repr(self))

  def get_vars(self): return set(self.symbol)