
import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic


all_agents = []
seed_frac = 0.1


def set_params(alphaI, trend_sensitivityI, seed_fracI, num_agentsI, num_neighborsI, update_probI):
    global alpha, trend_sensitivity, seed_frac, num_agents, num_neighbors, update_prob

    trend_sensitivity = trend_sensitivityI
    alpha = alphaI
    seed_frac = seed_fracI
    num_agents = num_agentsI
    num_neighbors = num_neighborsI
    update_prob = update_probI


class Agent:
    global all_agents

    def __init__(self):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0

        if random.random() < seed_frac:
            self.state = 1

    def eval_Neighbors(self, num_neighbors: int):
        self.neighbors = []
        _neighbor_set = set()

        while len(_neighbor_set) < num_neighbors:
            new_n = random.choice(all_agents)

            if new_n is not self and new_n not in _neighbor_set:
                _neighbor_set.add(new_n)

        self.neighbors = list(_neighbor_set)

    def eval_state(self, zetas):
        if random.random() > update_prob:
            return self.state

        _trend = random.random()

        if _trend > trend_sensitivity:
            if len(self.neighbors) == 0:
                raise ReferenceError('No neighbors found')

            # Count adopting neighbors
            _adopters = sum(n.state for n in self.neighbors)

            # Calculate payoffs directly
            _payoffInnov = _adopters * (1 + alpha)
            _payoffquo = len(self.neighbors) - _adopters

            if _payoffInnov > _payoffquo:
                return 1
            elif _payoffInnov < _payoffquo:
                return 0
            else:
                return self.state

        else:
            _zeta_current = zetas[-1]
            _zeta_prev = zetas[-2]

            if _zeta_current > _zeta_prev:
                return 1
            elif _zeta_current < _zeta_prev:
                return 0
            else:
                return self.state


def create_Agents(number: int):
    for _ in range(number):
        _tmp = Agent()


def eval_frac(lst: list) -> float:
    return sum(lst) / len(lst)


def evaluate_all_neighbors(agent_array: list[Agent], num: int):
    for agent in agent_array:
        agent.eval_Neighbors(num_neighbors=num_neighbors)


def run_sim(iterations: int, plot: bool) -> list[float]:
    global all_agents
    global num_agents

    # Initiate the Agents
    all_agents = []
    create_Agents(number=num_agents)

    all_states = [a.state for a in all_agents]
    fractions_array: list[float] = [0, 0]
    reps = 0
    points = []

    for timestep in range(iterations):

        # Calculate adoption fraction without creating an intermediate list
        fraction = sum(a.state for a in all_agents) / num_agents

        fractions_array.append(fraction)
        points.append(fraction)

        # Re-evaluate neighbors
        evaluate_all_neighbors(agent_array=all_agents, num=num_neighbors)

        # Calculate new states
        new_states = [
            agent.eval_state(zetas=fractions_array)
            for agent in all_agents
        ]

        # Update states simultaneously
        for agent, state in zip(all_agents, new_states):
            agent.state = state

        reps += 1

    if plot:
        plt.figure(figsize=(10, 10), num='adoption_curve_game_theoretic')
        plt.plot(np.linspace(1, reps, num=reps), points)
        plt.title(
            label=f'Output of the Game-Theoretic Model with Parameters '
                  f'alpha = {alpha}, s = {trend_sensitivity} and p = {update_prob}.'
        )
        plt.show()

    return points
""" set_params(alphaI=5.0, trend_sensitivityI=0.1, seed_fracI=0.1, num_agentsI=500, num_neighborsI=5, update_probI=0.5)
run_sim(iterations=15, plot=True) """