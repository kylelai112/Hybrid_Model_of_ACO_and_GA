import random

def cal_fitness(sol, weights, values, capacity):
    total_weight = 0
    total_value = 0
    for i in range(len(sol)):
        if sol[i] == 1:
            total_weight += weights[i]
            total_value += values[i]
    if total_weight > capacity:
        return 0
    else:
        return total_value


class ProblemSet01():
    def __init__(self):
        self.weights = [41, 50, 49, 59, 55, 57, 60]
        self.values = [442, 525, 511, 593, 546, 564, 617]
        self.opt = [0, 1, 0, 1, 0, 0, 1]
        self.capacity = 170


class ProblemSet02():
    def __init__(self):
        self.weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
        self.values = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
        self.opt = [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
        self.capacity = 165


class ProblemSet03():
    def __init__(self):
        self.weights = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
        self.values = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
        self.opt = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]
        self.capacity = 750


class ProblemSet04():
    def __init__(self):
        self.weights = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830,
                        610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]
        self.values = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992,
                       1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243,
                       466257, 369261]
        self.opt = [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
        self.capacity = 6404180


class ProblemSet05():
    def __init__(self):
        # randomly generate large number set
        itemsNum = 50
        self.weights = random.sample(range(10, 50000), itemsNum)
        self.values = random.sample(range(10, 50000), itemsNum)
        self.opt = []
        self.capacity = sum(self.weights)//3
        print(self.capacity)


k = ProblemSet05()
# v = cal_fitness(k.opt, k.weights, k.values, k.capacity)
