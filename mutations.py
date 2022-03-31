def Axiom(num, substitutions):
    if num == 0:
        return Operator('Implies', [substitutions[0], substitutions[0]], derived_by='Ax0')
    elif num == 1:
        return Operator('Implies', [substitutions[0], Operator('Implies', [substitutions[1], substitutions[0]] )], derived_by='Ax1')
    elif num == 2:
        return Operator('Implies', [Operator('Implies', [substitutions[0], Operator('Implies', [substitutions[1], substitutions[2]])]), Operator('Implies', [Operator('Implies', [substitutions[0], substitutions[1]]), \
                Operator('Implies', [substitutions[0], substitutions[2]])])], derived_by='Ax2')
    elif num == 3:
        return Operator('Implies', [Operator('Implies', [substitutions[0], substitutions[1]]), Operator('Implies', [Operator('Not', [substitutions[1]]), Operator('Not', [substitutions[0]])])], derived_by='Ax3')
    
def MP(op1, op2, individual):
    if op1.name == 'Implies' and op2 == op1.operands[0]:
        new_thm = Operator(op1.operands[1].name, op1.operands[1].operands, derived_from=[op1, op2], derived_by='MP')
        if new_thm not in individual.proof_seq:
            op1.derives.append(new_thm)
            op2.derives.append(new_thm)
            individual.add_step(new_thm)
            
    elif op2.name == 'Implies' and op1 == op2.operands[0]:
        new_thm = Operator(op2.operands[1].name, op2.operands[1].operands, derived_from=[op2, op1], derived_by='MP')
        if new_thm not in individual.proof_seq:
            op1.derives.append(new_thm)
            op2.derives.append(new_thm)
            individual.add_step(new_thm)


def mutate(possible_sol):
    AXP = 1 # 0.5
    RMP = 0 # 0.02
    ORP = 0 # 0.02
    ANP = 0 # 0.01
    if random.random() < AXP and not possible_sol.proven:
        #Invoke an axiom with a term seen in 'to-prove' or any derived term
        #print('Adding Axiom')

        # randomly select an axiom and 4 qualified substitute exprs
        ax_num = random.randint(0,3)
        subs   = []
        while len(subs) < 4:
            term_num = random.randint(0, len(prvr.terms)-1)
            term_candidate = prvr.terms[term_num]
            chance = random.random()
            if chance < (1/(term_candidate.height())):
                subs.append(prvr.terms[term_num])

        # invoke the axiom on the substitute exprs
        ax_cand = Axiom(ax_num, subs)
        prvr.add_step(ax_cand)

        # if ax_cand not in prvr.proof_seq:
        #     prvr.proof_seq.append(Axiom(ax_num, subs))
        #     prvr.proof_seq[0].set_line(1)
        #     prvr.proof_seq[0].get_terms(prvr.terms)
        #     prvr.check_last_thm()
        #     if prvr.thm_value(ax_cand) > prvr.conc_val:
        #         prvr.conclusion = ax_cand
        #         prvr.conc_val   = prvr.thm_value(ax_cand)
        #     if prvr.thm_value(ax_cand) > prvr.conc_val:
        #         prvr.conclusion = ax_cand
        #         prvr.conc_val   = prvr.thm_value(ax_cand)
        #print('Done Adding Axiom')
        
    if random.random() < RMP and len(prvr.proof_seq) > 2:
        print('Removing Branch')
        rmv = []
        indx = random.randint(1, len(prvr.proof_seq)-1)
        rmv.append(prvr.proof_seq[indx])
        k = 0
        print('k=',k)
        print(rmv)
        print(len(rmv))
        while k < len(rmv):
            for trm in rmv[k].derives:
                rmv.append(trm)
            k += 1
            print('k=',k)
            print(rmv)
            print(len(rmv))
        for trm in rmv:
            prvr.proof_seq.remove(trm)
            for i in range(len(prvr.proof_seq)-1):
                prvr.proof_seq[i].set_line(i)
        print('Done Removing')
        
    if random.random() < ORP and len(prvr.proof_seq) < MAX_LENGTH and not prvr.proven:
        #print('Or Instructions')
        trm_num = random.randint(0, len(prvr.init_terms)-1)
        thm_num = random.randint(0, len(prvr.proof_seq) -1)
        new_thm1 = prvr.proof_seq[thm_num]._clone()
        new_thm1.set_line(-1)
        new_thm2 = prvr.init_terms[trm_num]._clone()
        new_thm  = Operator('Or', [new_thm1, new_thm2])
        prvr.proof_seq.append(new_thm)
        #print('Done with Or')
    
def Rule(name, operand):
    if name == 'Double Negation':
        if operand.name == 'Not' and operand.operands[0].name == 'Not':
            new_thm = Operator(operand.operands[0].operands[0].name, operand.operands[0].operands[0], derived_from=[operand], derived_by='Double Negation')
            return new_thm
    #if name == '