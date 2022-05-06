import random

from ast_nodes import *

class Prover:
  def __init__(self, to_prove, premises=[]):
    self.to_prove = to_prove._clone()
    self.proven = False
    self.vars = self.to_prove.get_vars()
    self.statements = []
    self.premises = premises[:]

  def _clone(self):
    return copy.deepcopy(self)
  
  def __repr__(self):
      rep = "{" + str(self.premises) + "} |=H " + str(self.to_prove) + "\n"
      for step in self.statements:
          rep += str(step) + "\n"
      return rep

  def mutate(self):
    h = random.randint(0, self.to_prove.height())
    ax_num = random.randint(0,2)
    phi = self.rand_ast(h)
    psi = self.rand_ast(h)
    ax_cand = None
    if ax_num == 0:
      ax_cand = Implies(phi, Implies(psi, phi))
    elif ax_num == 1:
      gamma = self.rand_ast(h)
      ax_cand = Implies(Implies(phi, Implies(psi, gamma)), Implies(Implies(phi, psi), Implies(phi, gamma)))
    elif ax_num == 2:
      ax_cand = Implies(Implies(Negate(phi), Negate(psi)), Implies(psi, phi))
    self.statements.append(ax_cand)
    return self

  def deduce(self):
    for f in self.statements:
      if isinstance(f, Implies):
        for g in self.statements:
          if f.left == g:
            self.statements.append(f.right._clone())

  def solved(self):
    return self.statements[-1] == self.to_prove

  def rand_ast(self, h):
    if h == 0:
      return Wff(random.sample(self.vars, 1)[0])
    else:
      j = random.randint(0,1)
      if j == 0:
        return Negate(self.rand_ast(h-1))
      else:
        k = random.randint(0, h-1)
        l = random.randint(0,1)
        if l == 0:
          return Implies(left=self.rand_ast(h-1), right=self.rand_ast(k))
        else:
          return Implies(left=self.rand_ast(k), right=self.rand_ast(h-1))

      
  # def deduce(self):
  #     if self.to_prove is ImpNode:
  #         self.ACP.append(self.to_prove.operands[0]._clone())
  #         assumption = self.to_prove.operands[0]._clone()
  #         assumption.derived_by = "ACP"
  #         self.proof_seq.append(assumption)
  #         self.to_prove = self.to_prove.operands[1]._clone()
  
  
  # def thm_value(self, op1):
  #     if op1 == self.to_prove:
  #         return 50
  #     elif op1.includes_in_consequent(self.to_prove):
  #         return (1/(1+(op1.height() - self.to_prove.height())))
  #     else:
  #         return 0
          
  # def add_step(self, op):
  #     if op not in self.proof_seq:
  #         self.proof_seq.append(op)
  #         self.proof_seq[-1].get_terms(self.terms)
  #         self.check_last_thm()
  #         if self.thm_value(op) > self.conc_val:
  #             self.conclusion = op
  #             self.conc_val   = self.thm_value(op)
    #  if len(self.proof_seq) == 0:
    #       #print('enter if')
    #       ax_num = random.randint(0,3)
    #       subs   = []
    #       while len(subs) < 4:
    #           term_num = random.randint(0, len(self.terms)-1)
    #           term_candidate = self.terms[term_num]
    #           chance = random.random()
    #           if chance < (1/(term_candidate.height())):
    #               subs.append(self.terms[term_num])
    #       ax_cand = Axiom(ax_num, subs)
    #       self.add_step(ax_cand)
  # def fix_lines(self):
  #     for i in range(len(self.proof_seq)):
  #         self.proof_seq[i].set_line(i+1)
          
  # def check_proof(self):
  #     for line in self.proof_seq:
  #         if line == self.to_prove:
  #             self.proven=True
              
  # def check_last_thm(self):
  #     if self.proof_seq[-1] == self.to_prove and len(self.ACP) == 0:
  #         self.proven = True
  #     elif self.proof_seq[-1] == self.to_prove:
  #         antecedent    = self.ACP.pop()
  #         new_thm       = Operator("Implies", [antecedent, self.to_prove])._clone()
  #         self.to_prove = new_thm._clone()
  #         new_thm.derived_by = "CP"
  #         self.add_step(new_thm)
  #         self.check_last_thm()