import GameTheoreticModel as gtm
import numpy as np
from scipy.optimize import differential_evolution
from sklearn.metrics import mean_squared_error

seed_frac = 0
num_agents = 500
num_neighbors = 10
y_data = [0.06,0.11,0.12,0.35,0.55,0.62,0.69,0.72,0.77,0.8]
seed_frac = y_data[0]
iterations = len(y_data)

def run_gtm(parameters: list[int|float]) -> list[float]: # parameters: [alpha, trend_sensitivity, update_prob]
    print(f'running with parameters {parameters}')
    gtm.set_params(alphaI=parameters[0], trend_sensitivityI=parameters[1], seed_fracI=seed_frac, num_agentsI=num_agents, num_neighborsI=num_neighbors, update_probI=parameters[2])
    return gtm.run_sim(iterations=iterations, plot=False)

def objective(params):
    y_pred = run_gtm(parameters=params)
    return mean_squared_error(y_true=y_data, y_pred=y_pred)

bounds = [
    (3.0, 4.0),   # alpha
    (0.1, 0.3),   # trend_sensitivity
    (0.001, 0.4)    # update prob
]

solver = differential_evolution(func=objective, bounds=bounds, maxiter=1000, tol=0.001)

print(f'solution: {list(solver.x)}')
print(f'solution score: {solver.fun}')
