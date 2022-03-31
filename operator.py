"""
Operator class
"""
class Operator:
    
    def __init__(self, name, operands=[], line=-1, derived_from=[], derives=[], derived_by=""):
        self.name = name
        if self.name in ['And', 'Or', 'Implies', 'Eqivalent']:
            self.arity=2
        elif self.name in ['Not']:
            self.arity=1
        elif self.name in alphabet:
            self.arity=0
        else:
            print(self.name in alphabet)
            print(self.name)
            print(type(self.name))
        self.operands = operands[:self.arity]
        self.derived_from= derived_from
        self.derives = derives
        self.line = line
        self.derived_by=derived_by
        
    def set_line(self, line_num):
        self.line=line_num
        
    def _clone(self):
        return copy.deepcopy(self)
        
    def __repr__(self):
        
        if self.line != -1:
            this_op = str(self.line) + '. '
        else:
            this_op = ""
        if len(self.operands) > 1:
            this_op += '('
            this_op += str(self.operands[0])
            this_op += symbols[self.name]
            this_op += str(self.operands[1])
            this_op += ')'
        elif len(self.operands) == 1:
            this_op += symbols[self.name]
            this_op += str(self.operands[0])
        elif len(self.operands) == 0:
            this_op += self.name
        if self.line != -1:
            if len(self.derived_from) > 0:
                this_op += '\t ' + str([str(l.line) + ' ' for l in self.derived_from])
            this_op += '\t ' + self.derived_by
        
        
        return this_op
    
    def get_fn_repr(self):
        if self.line != -1:
            this_op = str(self.line) + '. ' + self.name
        else:
            this_op = self.name
        if len(self.operands) > 0:
            this_op += '('
            for op in self.operands:
                this_op += str(op)
            this_op += ')'
        if self.line != -1:
            if len(self.derived_from) > 0:
                this_op += '\t ' + str([str(l.line) + ' ' for l in self.derived_from])
            this_op += '\t ' + self.derived_by
        return this_op
    
    def get_vars(self, var_list=[]):
        if self.arity==0:
            var_list.append(self.name)
            return var_list
        else:
            for op in self.operands:
                op.get_vars(var_list)
            return var_list
        
    def height(self):
        if self.arity == 0:
            return 1
        else:
            return 1 + max([op.height() for op in self.operands])
    
    def get_terms(self, term_list=[]):
        if self not in term_list:
            cp = self._clone()
            cp.set_line(-1)
            term_list.append(cp)
        if self.arity == 0:
            return term_list
        else:
            for op in self.operands:
                op.get_terms(term_list)
            return term_list
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.operands == other.operands
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def includes(self, other):
        if self == other:
            return True
        elif (self.arity == 0 and self != other):
            return False
        else:
            for operand in self.operands:
                if operand.includes(other):
                    return True
            return False
        
    def includes_in_consequent(self, other):
        if self.name != 'Implies':
            return self.includes(other)
        if self == other:
            return True
        elif (self.arity == 0 and self != other):
            return False
        else:
            if self.operands[1].includes(other):
                return True
            return False