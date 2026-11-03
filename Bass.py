
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def bass_model(t, y, p, q):
    dydt = (p + q * y[0]) * (1 - y[0])
    return [dydt]


def solve_bass(p, q, y0, t_max, num_points): # p, q: parameters of the model, y0: fraction at timestep 0, t_max: maximum timestep, num_points: number of points between beginning and end

    t_eval = np.linspace(0, t_max, num_points)

    solution = solve_ivp(
        bass_model,
        t_span=(0, t_max),
        y0=[y0],
        args=(p, q),
        t_eval=t_eval,
        method="RK45",
        rtol=1e-8,
        atol=1e-10
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    return solution.t, solution.y[0]