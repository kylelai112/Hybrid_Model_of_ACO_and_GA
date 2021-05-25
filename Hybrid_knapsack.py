import knapsackData as ks
import random
from matplotlib import pyplot as plt
from time import time



class hybrid_algo():
    def __init__(self, prob_set, pop_size):
        self.prob_set = prob_set
        self.pop_size = pop_size
        self.alpha = 1
        self.beta = 1
        self.phe = []
        self.itemScore = []

        for i in range(len(self.prob_set.weights)):
            self.phe.append(1)
            score = self.prob_set.values[i] / self.prob_set.weights[i] ** 2
            self.itemScore.append(score)

    def cal_IS_probability(self, possible_weight_list):
        prob_value = [self.itemScore[i] ** self.alpha for i in range(len(self.phe)) if
                      self.prob_set.weights[i] in possible_weight_list]
        prob_list = [x / sum(prob_value) for x in prob_value]
        return prob_list

    def selectObject(self, prob_l, possible_weight_list):
        rand = random.random()
        # print(rand)
        select = 0
        for i in range(len(prob_l)):
            select += prob_l[i]
            if select > rand:
                return possible_weight_list[i]

    def gen_initial_pop(self):
        population = []
        while len(population) < self.pop_size:
            solution = []
            selected_weight = []
            possible_weight_list = list(self.prob_set.weights).copy()
            capacity_left = int(self.prob_set.capacity)
            while (capacity_left > 0 and len(possible_weight_list) != 0):
                prob_l = self.cal_IS_probability(possible_weight_list)
                weight_pick = self.selectObject(prob_l, possible_weight_list)
                selected_weight.append(weight_pick)
                capacity_left -= weight_pick
                possible_weight_list.remove(weight_pick)
                possible_weight_list = [x for x in possible_weight_list if x <= capacity_left]

            for i in self.prob_set.weights:
                if i in selected_weight:
                    solution.append(1)
                else:
                    solution.append(0)

            population.append(solution)
        return population

    def pop_with_fit(self, pop):
        fit_list = []
        for i in pop:
            fitness = ks.cal_fitness(i, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
            fit_list.append(fitness)
        pwf = list(zip(pop, fit_list))
        return pwf

    def random_select_parent(self, pop):
        p1 = list(random.choice(pop)).copy()
        p2 = list(random.choice(pop)).copy()
        while p1 == p2:
            p2 = self.mutation(p2)

        return p1, p2

    def cal_phe_probability(self, possible_weight_list):
        prob_value = [self.phe[i] ** self.beta for i in range(len(self.phe)) if
                      self.prob_set.weights[i] in possible_weight_list]
        prob_list = [x / sum(prob_value) for x in prob_value]
        return prob_list

    def update_phenomone(self, solution):
        delta_phe = 1
        evaporate_C = 0.95
        for i in range(len(solution)):
            self.phe[i] *= evaporate_C
            if solution[i] == 1:
                self.phe[i] += delta_phe

    def phe_guide_new_gen(self, pop):
        n_ge = []
        p1, p2 = self.random_select_parent(pop)
        p1Weight = [self.prob_set.weights[i] for i in range(len(p1)) if p1[i] == 1]
        p2Weight = [self.prob_set.weights[i] for i in range(len(p2)) if p2[i] == 1]

        selected_weight = []
        possible_p1weight_list = p1Weight.copy()
        possible_p2weight_list = p2Weight.copy()
        capacity_left = int(self.prob_set.capacity)
        while (capacity_left > 0):
            # select one from p1
            if len(possible_p1weight_list) != 0:
                prob_l = self.cal_phe_probability(possible_p1weight_list)
                weight_pick = self.selectObject(prob_l, possible_p1weight_list)
                selected_weight.append(weight_pick)
                capacity_left -= weight_pick
                possible_p1weight_list.remove(weight_pick)
                possible_p1weight_list = [x for x in possible_p1weight_list if x <= capacity_left]
                possible_p2weight_list = [x for x in possible_p2weight_list
                                          if (x <= capacity_left and x not in selected_weight)]


            # select one from p2
            if len(possible_p2weight_list) != 0:
                prob_l = self.cal_phe_probability(possible_p2weight_list)
                weight_pick = self.selectObject(prob_l, possible_p2weight_list)
                selected_weight.append(weight_pick)
                capacity_left -= weight_pick
                possible_p2weight_list.remove(weight_pick)
                possible_p2weight_list = [x for x in possible_p2weight_list if x <= capacity_left]
                possible_p1weight_list = [x for x in possible_p1weight_list
                                          if (x <= capacity_left and x not in selected_weight)]

            if len(possible_p1weight_list) == 0 and len(possible_p2weight_list) == 0:
                capacity_left = 0

        for i in self.prob_set.weights:
            if i in selected_weight:
                n_ge.append(1)
            else:
                n_ge.append(0)

        p1fit = ks.cal_fitness(p1, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
        p2fit = ks.cal_fitness(p2, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)
        n_gefit = ks.cal_fitness(n_ge, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)

        # update phetomone if child is better than parent
        if n_gefit > p1fit and n_gefit > p2fit:
            self.update_phenomone(n_ge)

        return n_ge

    def mutation(self, chromo):
        # guided mutation
        capacity_left = int(self.prob_set.capacity)
        selected_weights = [self.prob_set.weights[i] for i in range(len(chromo)) if chromo[i] == 1]
        possible_weight_list = [x for x in self.prob_set.weights if x not in selected_weights]
        largest_num = max(selected_weights)
        selected_weights.remove(largest_num)
        capacity_left -= sum(selected_weights)
        possible_weight_list = [x for x in possible_weight_list if x <= capacity_left]
        while len(possible_weight_list) != 0:
            prob_l = self.cal_phe_probability(possible_weight_list)
            weight_pick = self.selectObject(prob_l, possible_weight_list)
            selected_weights.append(weight_pick)
            capacity_left -= weight_pick
            possible_weight_list = [x for x in possible_weight_list if x <= capacity_left]

        mutated_chromo =[]
        for i in self.prob_set.weights:
            if i in selected_weights:
                mutated_chromo.append(1)
            else:
                mutated_chromo.append(0)

        return mutated_chromo

    def run(self):
        t_start = time()
        num_of_generation = 200
        new_child_num = 5
        new_gen = []
        fit_progress = []
        initial_ga_pop = list(self.gen_initial_pop()).copy()
        mutation_chance = 0.2
        for i in range(num_of_generation):
            # print("test", initial_ga_pop)
            for num in range(new_child_num):
                n_gen = self.phe_guide_new_gen(initial_ga_pop)
                new_gen.append(n_gen)
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
            # print('Gen', i, sort_pwf)

            fit_progress.append(sort_pwf[0][1])

            # elitism: only selct the top 5 as new pop
            initial_ga_pop.clear()
            for k in range(5):
                initial_ga_pop.append(list(sort_pwf[k][0]))

        for i in range(1):
            print("Hybrid Best solution: ")
            print(sort_pwf[i])

        t_finish = time()
        solving_time = (t_finish - t_start)
        print("Hybrid time taken: ", "%.5f" % solving_time)

        plt.figure(0)
        # plt.subplot(3, 1, 3)
        # plt.title(label="Hybric")
        plt.plot(fit_progress,color='#F6BE00', linestyle='solid', marker='*', label="Hybrid")
        plt.xlabel('Generation/Iteration')
        plt.ylabel('Best fitness')
        plt.legend(loc='lower right')
        plt.show()




initial_pop_size = 5

testh = hybrid_algo(ks.k, initial_pop_size)


testh.run()
