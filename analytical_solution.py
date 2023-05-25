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
    C = sp.nsolve(C/2 - right_part - residual, C, 100000)  # 100000 here is the initial value for numerical solution,
                                                           # the reason for such a big value is to avoid trivial root: 0
    ret = [(C/2 + (k+1)*A + B*sp.Sum(1-sp.exp((-C)*lambdas[i]), (i, 0, k-1))).doit() for k in range(nfloor)]
    return np.array(C), np.array(ret)


if __name__ == '__main__':
    nfloor = 21
    lambdas = [0.005]*nfloor
    A = 2
    B = 10
    C, T = solver(nfloor, lambdas, A, B)
    print('C:', C)
    print('T:\n', list(map(round, T)))
    # ET: expected value of the time spend on the elevator for all people
    ET = np.sum(np.array(lambdas)/sum(lambdas) * np.array(T))
    print('ET:', ET)