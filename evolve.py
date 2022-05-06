import random
from parser import parse_proof
from prover import Prover

POP_SIZE = 10

def main():
    to_prove = "(A => A)"

    ast = parse_proof(to_prove)
    print(ast)
    height = ast.height()
    print(ast.get_vars())

    population = [Prover(ast) for i in range(POP_SIZE)]
    max_fit = 0
    best_proof = None

    for gen in range(40):
        print(f'Generation: {gen}')

        [x.mutate() for x in population]
        [x.deduce() for x in population]
        [print("Solved") for x in population if x.solved()]
    #     curr_gen_fit = []
    #     for i in range(POP_SIZE):
    #         # Evaluate fitness of the ith population member and save it
    #         curr_fit = fit(population[i])
    #         curr_gen_fit.append(curr_fit)
    #         if (curr_fit > max_fit):
    #             max_fit = curr_fit
    #             best_proof = population[i]._clone()
    #             print('-----New Best Fitness!-----')
    #             print(max_fit)
    #             print(best_proof.proof_seq)
        
    #     print('-----Producing Next Generation-----')
    #     # initialize next generation using the five best solutions
    #     next_gen = []
    #     sorted_by_fit = sorted(range(len(curr_gen_fit)), key=lambda x: curr_gen_fit[x], reverse=True)
    #     next_gen += [population[sorted_by_fit[i]]._clone() for i in range(5)]
        
    #     # until we reach the population size, continue to add random solutions
    #     while len(next_gen) < POP_SIZE:
    #         ind1 = random.randint(0, POP_SIZE-1)
    #         ind2 = random.randint(0, POP_SIZE-1)
    #         if ind1 > ind2:
    #             next_gen.append(population[sorted_by_fitness[ind1]]._clone())
    #         else:
    #             next_gen.append(population[sorted_by_fitness[ind2]]._clone())
        
    #     for solution in next_gen:
    #         mutate(solution)
            
    #         # randomly deduce
    #         if random.random() < DEDUCE_P:
    #             solution.deduce()
    #         if not ind.proven and ind.conclusion.name == 'Implies':
    #                 for i in range(len(ind.proof_seq)):
    #                     if ind.proof_seq[i] == ind.conclusion.operands[0]:
    #                         #print('Modus Ponens')
    #                         MP(ind.proof_seq[i], ind.conclusion, ind)
    #                         #ind.add_step(cand)

    #         for k in range(4):
    #             inst = random.randint(0, len(ind.proof_seq)-1)
    #             if  not ind.proven and ind.proof_seq[inst].name == 'Implies':
    #                 for i in range(len(ind.proof_seq)):
    #                     if ind.proof_seq[i] == ind.proof_seq[inst].operands[0]:
    #                         #print('Modus Ponens')
    #                         MP(ind.proof_seq[i], ind.proof_seq[inst], ind)
    #                         #ind.add_step(cand)
    #                         # if cand not in ind.proof_seq:
    #                         #     ind.proof_seq.append(MP(ind.proof_seq[i], ind.proof_seq[inst]))
    #                         #     ind.check_last_thm()
    #                     #print('Modus Ponens Done!')
    #     #print('To next gen')
    #     population = next_gen
    #     generation += 1
        
    # for prvr in population:
    #     prvr.fix_lines()
    # print("Done")

if __name__ == '__main__':
    main()
