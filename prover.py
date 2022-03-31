"""
Prover class 
"""
class Prover:
    
    def __init__(self, to_prove, premises=[]):
        self.conclusion= None
        self.conc_val  = -1
        self.to_prove  = to_prove._clone()
        self.proven    = False
        self.alphabet  = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.vars      = self.to_prove.get_vars()
        self.init_terms= self.to_prove.get_terms()
        self.terms     = self.to_prove.get_terms()
        self.available = [v for v in alphabet if v not in self.vars]
        self.premises  = premises[:]
        self.proof_seq = premises[:]
        self.ACP       = []
        if len(self.proof_seq) == 0:
            #print('enter if')
            ax_num = random.randint(0,3)
            subs   = []
            while len(subs) < 4:
                term_num = random.randint(0, len(self.terms)-1)
                term_candidate = self.terms[term_num]
                chance = random.random()
                if chance < (1/(term_candidate.height())):
                    subs.append(self.terms[term_num])
            ax_cand = Axiom(ax_num, subs)
            self.add_step(ax_cand)
       
    def deduce(self):
        if self.to_prove.name == "Implies":
            self.ACP.append(self.to_prove.operands[0]._clone())
            assumption = self.to_prove.operands[0]._clone()
            assumption.derived_by = "ACP"
            self.proof_seq.append(assumption)
            self.to_prove = self.to_prove.operands[1]._clone()
    
    
    def thm_value(self, op1):
        if op1 == self.to_prove:
            return 50
        elif op1.includes_in_consequent(self.to_prove):
            return (1/(1+(op1.height() - self.to_prove.height())))
        else:
            return 0
            
    def add_step(self, op):
        if op not in self.proof_seq:
            self.proof_seq.append(op)
            self.proof_seq[-1].get_terms(self.terms)
            self.check_last_thm()
            if self.thm_value(op) > self.conc_val:
                self.conclusion = op
                self.conc_val   = self.thm_value(op)
    
    
    def _clone(self):
        return copy.deepcopy(self)
    
    def __repr__(self):
        rep = ""
        rep += "To Prove: " + str(self.to_prove) + "\n"
        for step in self.proof_seq:
            rep += str(step)
            rep += "\n"
        rep += "--- Therefore ---\n" + str(self.conclusion)
        return rep
    
    def fix_lines(self):
        for i in range(len(self.proof_seq)):
            self.proof_seq[i].set_line(i+1)
            
    def check_proof(self):
        for line in self.proof_seq:
            if line == self.to_prove:
                self.proven=True
                
    def check_last_thm(self):
        if self.proof_seq[-1] == self.to_prove and len(self.ACP) == 0:
            self.proven = True
        elif self.proof_seq[-1] == self.to_prove:
            antecedent    = self.ACP.pop()
            new_thm       = Operator("Implies", [antecedent, self.to_prove])._clone()
            self.to_prove = new_thm._clone()
            new_thm.derived_by = "CP"
            self.add_step(new_thm)
            self.check_last_thm()

