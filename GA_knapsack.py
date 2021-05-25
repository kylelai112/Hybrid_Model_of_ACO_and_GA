import knapsackData as ks
import random
from matplotlib import pyplot as plt
from time import time


class genetic_algo():
    def __init__(self, prob_set, pop_size):
        self.prob_set = prob_set
        self.pop_size = pop_size

    def gen_initial_pop(self):
        population = []
        while len(population) < self.pop_size:
            indi_weight = self.prob_set.capacity + 1
            while indi_weight > self.prob_set.capacity:
                indi_sol = [random.randint(0, 1) for x in range(0, len(self.prob_set.weights))]
                indi_weight = 0
                for i in range(len(indi_sol)):
                    if indi_sol[i] == 1:
                        indi_weight += self.prob_set.weights[i]
                if indi_weight <= self.prob_set.capacity:
                    population.append(indi_sol)
        return population

    def pop_with_fit(self, pop):
        fit_list = []
        for i in pop:
            fitness = ks.cal_fitness(i, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
            fit_list.append(fitness)
        pwf = list(zip(pop, fit_list))
        return pwf

    def tournament(self, pop):
        p1 = list(random.choice(pop)).copy()
        p2 = list(random.choice(pop)).copy()
        p1fit = ks.cal_fitness(p1, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
        p2fit = ks.cal_fitness(p2, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
        if p1fit >= p2fit:
            return p1
        return p2

    def cxOrdered(self, ind1, ind2):
        """Executes an ordered crossover (OX) on the input
        individuals. The two individuals are modified in place. This crossover
        expects :term:`sequence` individuals of indices, the result for any other
        type of individuals is unpredictable.
        :param ind1: The first individual participating in the crossover.
        :param ind2: The second individual participating in the crossover.
        :returns: A tuple of two individuals.
        Moreover, this crossover generates holes in the input
        individuals. A hole is created when an attribute of an individual is
        between the two crossover points of the other individual. Then it rotates
        the element so that all holes are between the crossover points and fills
        them with the removed elements in order. For more details see
        [Goldberg1989]_.
        This function uses the :func:`~random.sample` function from the python base
        :mod:`random` module.
        .. [Goldberg1989] Goldberg. Genetic algorithms in search,
           optimization and machine learning. Addison Wesley, 1989
        """
        size = min(len(ind1), len(ind2))
        a, b = random.sample(range(size), 2)
        if a > b:
            a, b = b, a

        holes1, holes2 = [True] * size, [True] * size
        for i in range(size):
            if i < a or i > b:
                holes1[ind2[i]] = False
                holes2[ind1[i]] = False

        # We must keep the original values somewhere before scrambling everything
        temp1, temp2 = ind1, ind2
        k1, k2 = b + 1, b + 1
        for i in range(size):
            if not holes1[temp1[(i + b + 1) % size]]:
                ind1[k1 % size] = temp1[(i + b + 1) % size]
                k1 += 1

            if not holes2[temp2[(i + b + 1) % size]]:
                ind2[k2 % size] = temp2[(i + b + 1) % size]
                k2 += 1

        # Swap the content between a and b (included)
        for i in range(a, b + 1):
            ind1[i], ind2[i] = ind2[i], ind1[i]

        return ind1, ind2

    def generate_new_gen(self, pop):
        n_ge = []
        for i in range(len(pop)):
            p1 = self.tournament(pop)
            p2 = self.tournament(pop)

            c1, c2 = self.cxOrdered(p1, p2)

            n_ge.append(c1)
            n_ge.append(c2)

        return list(n_ge)

    def mutation(self, chromo):
        num_mutation_chromo = 2
        for i in range(num_mutation_chromo):
            r = random.randint(0, len(chromo) - 1)
            if chromo[r] == 1:
                chromo[r] = 0
            else:
                chromo[r] = 1
        return chromo

    def run(self):
        t_start = time()
        num_of_generation = 200
        fit_progress = []
        initial_ga_pop = list(self.gen_initial_pop()).copy()
        mutation_chance = 0.2
        all_pop = []
        for i in range(num_of_generation):
            # print("test", initial_ga_pop)
            new_gen = self.generate_new_gen(initial_ga_pop)
            # print("ngen", new_gen)
            # print("test1", initial_ga_pop)
            all_pop = initial_ga_pop + new_gen
            # print("all_pop", i, all_pop)
            # apply mutation
            for j in range(len(all_pop)):
                if mutation_chance > random.random():
                    all_pop.append(self.mutation(all_pop[j].copy()))

            pwf = self.pop_with_fit(all_pop)
            sort_pwf = sorted(pwf, key=lambda x: x[1], reverse=True)

            fit_progress.append(sort_pwf[0][1])

            # elitism: only selct the top 5 as new pop
            initial_ga_pop.clear()
            for k in range(5):
                initial_ga_pop.append(list(sort_pwf[k][0]))

        for i in range(1):
            print("GA Best solution: ")
            print(sort_pwf[i])
        t_finish = time()
        solving_time = (t_finish - t_start)
        print("GA time taken: ", "%.5f" % solving_time)

        plt.figure(0)
        # plt.subplot(3, 1, 1)
        plt.title(label="Intelligent Algorithm")
        plt.plot(fit_progress, color='blue', linestyle='dashed', marker='o', label="GA")
        plt.xlabel('Generation')
        plt.ylabel('Best fitness')
        # plt.show()


initial_pop_size = 5

testga = genetic_algo(ks.k, initial_pop_size)
testga.run()
