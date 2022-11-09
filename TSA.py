#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/8 14:41
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : TSA.py
# @Statement : Tree-Seed Algorithm
# @Reference : Mustafa Servet Kiran. TSA: Tree-seed algorithm for continuous optimization[J]. Expert Systems with Applications, 2015, 6686-6698.
import random
import math
import matplotlib.pyplot as plt


def obj(x):
    """
    The objective function of pressure vessel design
    :param x:
    :return:
    """
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    x4 = x[3]
    g1 = -x1 + 0.0193 * x3
    g2 = -x2 + 0.00954 * x3
    g3 = -math.pi * x3 ** 2 - 4 * math.pi * x3 ** 3 / 3 + 1296000
    g4 = x4 - 240
    if g1 <= 0 and g2 <= 0 and g3 <= 0 and g4 <= 0:
        return 0.6224 * x1 * x3 * x4 + 1.7781 * x2 * x3 ** 2 + 3.1661 * x1 ** 2 * x4 + 19.84 * x1 ** 2 * x3
    else:
        return 1e10


def boundary_check(value, lb, ub):
    """
    The boundary check
    :param value:
    :param lb: the lower bound (list)
    :param ub: the upper bound (list)
    :return:
    """
    for i in range(len(value)):
        value[i] = max(value[i], lb[i])
        value[i] = min(value[i], ub[i])
    return value


def main(pop, iter, lb, ub, ST):
    """
    The main function of the TSA
    :param pop: the number of trees
    :param iter: the iteration number
    :param lb: the lower bound (list)
    :param ub: the upper bound (list)
    :param ST: search tendency
    :return:
    """
    # Step 1. Initialization
    pos = []  # the position of all trees
    score = []  # the score of all trees
    dim = len(lb)  # dimension
    for i in range(pop):
        temp_pos = [random.uniform(lb[j], ub[j]) for j in range(dim)]
        pos.append(temp_pos)
        score.append(obj(temp_pos))
    iter_best = []
    gbest = min(score)  # the score of the best-so-far tree
    gbest_pos = pos[score.index(gbest)].copy()  # the position of the best-so-far tree
    iter_con = 0

    # Step 2. The main loop
    for t in range(iter):
        for i in range(pop):

            # Step 2.1. Generate seeds
            seed_num = round(random.uniform(0.1, 0.25) * pop)  # the number of seeds produced by the ith tree
            seed_pos = []  # the position of the seeds of the ith tree
            seed_score = []  # the score of the seeds of the ith tree
            for _ in range(seed_num):
                temp_pos = []
                random_pos = random.choice(pos).copy()
                while random_pos == pos[i]:
                    random_pos = random.choice(pos).copy()
                for j in range(dim):
                    if random.random() < ST:
                        temp_pos.append(pos[i][j] + random.uniform(-1, 1) * (gbest_pos[j] - random_pos[j]))
                    else:
                        temp_pos.append(pos[i][j] + random.uniform(-1, 1) * (pos[i][j] - random_pos[j]))
                temp_pos = boundary_check(temp_pos, lb, ub)
                seed_pos.append(temp_pos)
                seed_score.append(obj(temp_pos))

            # Step 2.2. Substitute trees
            min_score = min(seed_score)
            if min_score < score[i]:
                pos[i] = seed_pos[seed_score.index(min_score)].copy()
                score[i] = min_score

        # Step 2.3. Update the global best
        if min(score) < gbest:
            min_score = min(score)
            gbest_pos = pos[score.index(min_score)].copy()
            gbest = min_score
            iter_con = t + 1
        iter_best.append(gbest)

    # Step 3. Sort the results
    x = [i for i in range(iter)]
    plt.figure()
    plt.plot(x, iter_best, linewidth=2, color='blue')
    plt.xlabel('Iteration number')
    plt.ylabel('Global optimal value')
    plt.title('Convergence curve')
    plt.show()
    return {'best score': gbest, 'best solution': gbest_pos, 'convergence iteration': iter_con}


if __name__ == '__main__':
    # Parameter settings
    pop = 10
    iter = 1000
    lb = [0, 0, 10, 10]
    ub = [99, 99, 200, 200]
    ST = 0.1
    print(main(pop, iter, lb, ub, ST))
