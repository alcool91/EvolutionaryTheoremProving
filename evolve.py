from parser import parse_proof


def main():
    POP_SIZE = 45
    DEDUCE_P = 0.2

    to_prove_a =    """
                    (p => (q => r)) => (q => (p => r))
                    """
    to_prove_b =    """
                    ((b)=>(c)) => ()

                    """

    ast = parse_proof(to_prove)
    print(ast)

    population = [Prover(ast._clone()) for i in range(POP_SIZE)]
    gen = 1
    max_fit = 0
    best_proof = None

    while generation < 5:
        print(f'Generation: {gen}')
        this_gen_fit = []
        for i in range(POP_SIZE):
            # Evaluate fitness of the ith population member and save it
            curr_fit = fit(population[i]
            this_gen_fit.append(curr_fit)
            if (curr_fit > max_fit):
                max_fit = curr_fit
                best_proof = population[i]._clone()
                print('-----New Best Fitness!-----')
                print(max_fit)
                print(best_proof.proof_seq)
        
        print('-----Producing Next Generation-----')
        # initialize next generation using the five best solutions
        next_gen = []
        sorted_by_fit = sorted(range(len(this_gen_fit)), key=lambda x: this_gen_fit[x], reverse=True)
        next_gen += [population[sorted_by_fit[i]]._clone() for i in range(5)]
        
        # until we reach the population size, continue to add random solutions
        while len(next_gen) < POP_SIZE:
            ind1 = random.randint(0, POP_SIZE-1)
            ind2 = random.randint(0, POP_SIZE-1)
            if ind1 > ind2:
                next_gen.append(population[sorted_by_fitness[ind1]]._clone())
            else:
                next_gen.append(population[sorted_by_fitness[ind2]]._clone())
        
        for solution in next_gen:
            mutate(solution)
            
            # randomly deduce
            if random.random() < DEDUCE_P:
                solution.deduce()
            if not ind.proven and ind.conclusion.name == 'Implies':
                    for i in range(len(ind.proof_seq)):
                        if ind.proof_seq[i] == ind.conclusion.operands[0]:
                            #print('Modus Ponens')
                            MP(ind.proof_seq[i], ind.conclusion, ind)
                            #ind.add_step(cand)

            for k in range(4):
                inst = random.randint(0, len(ind.proof_seq)-1)
                if  not ind.proven and ind.proof_seq[inst].name == 'Implies':
                    for i in range(len(ind.proof_seq)):
                        if ind.proof_seq[i] == ind.proof_seq[inst].operands[0]:
                            #print('Modus Ponens')
                            MP(ind.proof_seq[i], ind.proof_seq[inst], ind)
                            #ind.add_step(cand)
                            # if cand not in ind.proof_seq:
                            #     ind.proof_seq.append(MP(ind.proof_seq[i], ind.proof_seq[inst]))
                            #     ind.check_last_thm()
                        #print('Modus Ponens Done!')
        #print('To next gen')
        population = next_gen
        generation += 1
        
    for prvr in population:
        prvr.fix_lines()
    print("Done")

if __name__ == 'main':
  main()

def fit(prvr):
    fitness = 0
    conc = prvr.conclusion
    if conc.includes_in_consequent(prvr.to_prove):
        fitness += 1/(1+(conc.height() - prvr.to_prove.height()))
    if conc == prvr.to_prove:
        fitness += 6 + MAX_LENGTH - len(prvr.proof_seq)
    return fitness