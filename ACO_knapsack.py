import knapsackData as ks
import random
from matplotlib import pyplot as plt
from time import time


class AntColonyOptimization_algo():
    def __init__(self, prob_set):
        self.prob_set = prob_set
        self.alpha = 0.7
        self.beta = 0.8
        self.phe = []
        self.itemScore = []

        for i in range(len(self.prob_set.weights)):
            self.phe.append(1)
            score = self.prob_set.values[i] / self.prob_set.weights[i] ** 2
            self.itemScore.append(score)

    def cal_probability(self, possible_weight_list):
        prob_value = [self.phe[i] ** self.beta * self.itemScore[i] ** self.alpha
                      for i in range(len(self.phe)) if self.prob_set.weights[i] in possible_weight_list]
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

    def generate_solution(self):
        solution = []
        selected_weight = []
        possible_weight_list = list(self.prob_set.weights).copy()
        capacity_left = int(self.prob_set.capacity)
        while (capacity_left > 0 and len(possible_weight_list) != 0):
            prob_l = self.cal_probability(possible_weight_list)
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

        profit = ks.cal_fitness(solution, self.prob_set.weights, self.prob_set.values, self.prob_set.capacity)

        return solution, profit

    def update_phenomone(self, solution, profit, best_profit):
        delta_phe = 1 / (1 + (best_profit - profit) / best_profit)
        evaporate_C = 0.95
        for i in range(len(solution)):
            self.phe[i] *= evaporate_C
            if solution[i] == 1:
                self.phe[i] += delta_phe

    def run(self, antNum, iteration):
        t_start = time()
        best_profit = 1
        best_sol = []
        fit_progress = []
        for i in range(iteration):
            for j in range(antNum):
                solution, profit = self.generate_solution()
                self.update_phenomone(solution, profit, best_profit)
                # print(self.phe)
                if profit > best_profit:
                    best_profit = profit
                    best_sol = solution.copy()
            fit_progress.append(best_profit)

        print("ACO Best solution: ")
        print(best_sol, best_profit)
        t_finish = time()
        solving_time = (t_finish - t_start)
        print("ACO time taken: ", "%.5f" % solving_time)

        plt.figure(0)
        # plt.subplot(3, 1, 2)
        # plt.title(label="ACO")
        plt.plot(fit_progress, color='green', linestyle='dashdot', marker='x', label="ACO")
        plt.xlabel('Generation')
        plt.ylabel('Best fitness')
        # plt.show()


iteration = 200
antNum = 5

testaco = AntColonyOptimization_algo(ks.k)

testaco.run(antNum, iteration)
