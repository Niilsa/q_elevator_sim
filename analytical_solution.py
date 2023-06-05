import sys
import sympy as sp
import numpy as np


def solver(nfloor, lambdas, A, B, residual=0):
    """
    :param nfloor: num of floor the elevator can reach (**EXCLUDE** the first floor, e.g. 21 for all levels elevator in
                   information building).
    :param lambdas: arrival rate (unit: persons/s) for each floor, its dim should be equal to nfloor.
    :param A: the time (unit: s) spend on lifting one floor.
    :param B: the time (unit: s) spend on opening and closing elevator door.
    :param residual: not zero only for higher floors elevator, refers to the time (unit: s) spends on going through
                     unstoppable floors.
    :return: (C, T) where C: the average time for one lifting (i.e. time interval between the elevator leaves the first
                             floor and returns to the first floor)
                          T: a numpy array with nfloor dimensions, the i-th value indicates the average time (unit: s)
                             spend on the elevator for the people who go to i-th floor.
    """

    C = sp.Symbol('C')
    i = sp.Symbol('i')
    j = sp.Symbol('j')
    raw_lambdas = lambdas
    lambdas = sp.Array(raw_lambdas)
    lambdas_rev = sp.Array(np.flip(raw_lambdas))
    right_part_element = sp.exp((-C)*sp.Sum(lambdas_rev[i], (i, 0, j-1))) * (1-sp.exp((-C)*lambdas_rev[j])) * ((nfloor-j)*A + B*sp.Sum(1-sp.exp((-C)*lambdas[i]), (i, 0, nfloor-1-j-1)))
    right_part = sp.Sum(right_part_element, (j, 0, nfloor-1))
    C = sp.nsolve(C/2 - right_part - residual, C, 1000)  # 1000 here is the initial value for numerical solution,
                                                           # the reason for such a big value is to avoid trivial root: 0

    # probability_sum = sp.Sum(sp.exp((-C) * sp.Sum(lambdas_rev[i], (i, 0, j - 1))) * (1 - sp.exp((-C) * lambdas_rev[j])),
    #                          (j, 0, nfloor - 1)).doit()
    # print(f'prob sum: {probability_sum}')

    ret = [(C/2 + (k+1)*A + B*sp.Sum(1-sp.exp((-C)*lambdas[i]), (i, 0, k-1)) + residual).doit() for k in range(nfloor)]
    return np.array(C), np.array(ret)


if __name__ == '__main__':
    # nfloor = 21  # exclude the 1st floor
    # lambdas = [0.005]*nfloor
    # A = 2
    # B = 10
    # C, T = solver(nfloor, lambdas, A, B)
    # print('C:', C)
    # print('T:\n', T)
    # # ET: expected value of the time spend on the elevator for all people
    # ET = np.sum(np.array(lambdas)/sum(lambdas) * np.array(T))
    # print('ET:', ET)



    # for i in range(21):
    #     lambda_per_floor = 0.005 + 0.001 * i
    #     A = 2
    #     B = 10
    #
    #     print(f'lambda={lambda_per_floor:.4f}')
    #
    #     # 2 general
    #     nfloor = 21
    #     lambdas = [lambda_per_floor/2] * nfloor
    #     _, T = solver(nfloor, lambdas, A, B)
    #     ET = np.sum(np.array(lambdas) / sum(lambdas) * np.array(T))
    #     print(f'2 general: {ET:.2f}')
    #
    #     # 2 split
    #     nfloor_low = 11
    #     lambdas_low = [lambda_per_floor] * nfloor_low
    #     _, T_low = solver(nfloor_low, lambdas_low, A, B)
    #     nfloor_high = 10
    #     lambdas_high = [lambda_per_floor] * nfloor_high
    #     _, T_high = solver(nfloor_high, lambdas_high, A, B, residual=nfloor_low*A)
    #     ET_low = np.sum(np.array(lambdas_low) / sum(lambdas_low) * np.array(T_low))
    #     ET_high = np.sum(np.array(lambdas_high) / sum(lambdas_high) * np.array(T_high))
    #     ET = (np.sum(np.array(lambdas_high) * np.array(T_high)) + np.sum(np.array(lambdas_low) * np.array(T_low)))/(np.sum(lambdas_high)+np.sum(lambdas_low))
    #     print(f'1 low & 1 high: low {ET_low:.2f}, high {ET_high:.2f}, overall {ET:.2f}')
    #     print()

    for i in range(21):
        nfloor_low = 11
        lambdas_low = [0.005] * nfloor_low
        nfloor_high = 10
        lambdas_high = [0.005+i*0.0005] * nfloor_high
        lambda_overall = (lambdas_low + lambdas_high)

        A = 2
        B = 10


        print(f'lambda_low={lambdas_low[0]:.4f}; lambda_high={lambdas_high[0]:.4f}')

        # 2 general
        nfloor = 21
        lambdas = [tt/2 for tt in lambda_overall]
        _, T = solver(nfloor, lambdas, A, B)
        ET = np.sum(np.array(lambdas) / sum(lambdas) * np.array(T))
        print(f'2 general: {ET:.2f}')

        # 2 split
        _, T_low = solver(nfloor_low, lambdas_low, A, B)
        _, T_high = solver(nfloor_high, lambdas_high, A, B, residual=nfloor_low * A)

        ET_low = np.sum(np.array(lambdas_low) / sum(lambdas_low) * np.array(T_low))
        ET_high = np.sum(np.array(lambdas_high) / sum(lambdas_high) * np.array(T_high))
        ET = (np.sum(np.array(lambdas_high) * np.array(T_high)) + np.sum(np.array(lambdas_low) * np.array(T_low))) / (
                    np.sum(lambdas_high) + np.sum(lambdas_low))
        print(f'1 low & 1 high: low {ET_low:.2f}, high {ET_high:.2f}, overall {ET:.2f}')
        print()




