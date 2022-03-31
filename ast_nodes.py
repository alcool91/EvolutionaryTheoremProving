import abc

class ASTNode(abc.ABC):
  def __init__(self, name, children=None):
    self.name = name
    self.children = children if children else []

  def __repr(self):
    res = type(self).__name__
    if self.children:
      children_reprs = [repr(child) for child in self.children]
      children_lines = '\n'.join(children_reprs)
      children_lines_tabbed = map(lambda x: '\t' + x, children_lines.splitlines())
      res += '\n' + '\n'.join(children_lines_tabbed)
    return res

    @abc.abstractmethod
    def compile(self, symbol_table): pass

class UnaryExpr(ASTNode):
  def __init__(self, name, children):
    super().__init__(name, children=children)

  def compile(self, symbol_table): pass

class BinaryExpr(ASTNode):
  def __init__(self, children):
    super().__init__(children=children)

  def compile(self, symbol_table): pass