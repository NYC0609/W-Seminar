import LinearThresholdModel as ltm
import numpy as np
from scipy.optimize import minimize, differential_evolution
from sklearn.metrics import mean_squared_error

seed_frac = 0
num_agents = 500
num_neighbors = 10
y_data = [0.01, 0.024, 0.043, 0.064, 0.094, 0.128, 0.171, 0.216, 0.247, 0.293, 0.342, 0.411, 0.494, 0.517, 0.56, 0.63, 0.72, 0.718, 0.709, 0.696, 0.675, 0.691, 0.712, 0.766, 0.792, 0.864, 0.867, 0.892, 0.904, 0.924, 0.941, 0.96, 0.973, 0.977, 0.98, 0.982, 0.983, 0.995, 0.991, 0.993, 0.995, 0.996, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999, 0.999, 0.998, 0.997]
seed_frac = y_data[0]
iterations = len(y_data)

def run_ltm(parameters: list[int|float]) -> list[float]: # parameters: [mean, stdev, num_neighbors, update_prob]
    print(f'running with parameters {parameters}')
    ltm.set_params(meanI=parameters[0], stdevI=parameters[1], seed_fracI=seed_frac, num_agentsI=num_agents, num_neighborsI=num_neighbors, update_probI=parameters[2])
    return ltm.run_sim(iterations=iterations, plot=False)

def objective(params):
    y_pred = run_ltm(parameters=params)
    return mean_squared_error(y_true=y_data, y_pred=y_pred)

bounds = [
    (0.001, 0.8),   # mean
    (0.001, 0.3),   # standard dev
    (0.001, 0.6)    # update prob
]

solver = differential_evolution(func=objective, bounds=bounds, maxiter=300, tol=0.001)

print(f'solution: {list(solver.x)}')
print(f'solution score: {solver.fun}')
