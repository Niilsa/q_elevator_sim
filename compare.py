from analytical_solution import solver as analytical_solver
from elevator_simulation_2_general import solver as simulation_solver
import numpy as np


for i in range(21):
    lambda_value = 0.01 + 0.001*i
    print(f'lambda={np.round(lambda_value, 4):.4f}', end=': ')

    nfloor = 21  # exclude the 1st floor
    lambdas = [lambda_value] * nfloor
    A = 2
    B = 10

    C, T = analytical_solver(nfloor, lambdas, A, B)
    # ET: expected value of the time spend on the elevator for all people
    ET_ana = np.sum(np.array(lambdas) / sum(lambdas) * np.array(T))
    print(f'analytical result: {round(ET_ana, 2):.2f}', end='; ')

    ET_sim = simulation_solver(lambda_value*nfloor)
    print(f'simulation result: {round(ET_sim, 2):.2f}')

