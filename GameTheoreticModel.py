import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic


all_agents = []
seed_frac = 0.1 # number of seed agents

def set_params(alphaI, trend_sensitivityI, seed_fracI, num_agentsI, num_neighborsI, update_probI):
    global alpha # relative advantage
    global trend_sensitivity     # trend sensitivity
    global seed_frac
    global num_agents
    global num_neighbors
    global update_prob
    
    trend_sensitivity = trend_sensitivityI
    alpha = alphaI
    seed_frac = seed_fracI # initial adopters
    num_agents = num_agentsI
    num_neighbors = num_neighborsI
    update_prob = update_probI

class Agent:
    global all_agents
    
    def __init__(self):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0 # 0 -> has not adopted the innovation, 1 -> has adopted the innovation
        if random.random() < seed_frac:
            self.state = 1
    
    def eval_Neighbors(self, num_neighbors: int):
        self.neighbors = []
        for _ in range(num_neighbors):
            new_n = random.choice(all_agents)
            while new_n in self.neighbors or new_n == self:
                new_n = random.choice(all_agents)
            self.neighbors.append(new_n)
    
    def eval_state(self, zetas): # zetas: the list of the fractions of adopters at each timestep. Used for trend-sensitivity.
        if random.random() > update_prob:
            return self.state
        _trend = random.random()
        if _trend > trend_sensitivity: # update based on payoff
            _payoffInnov = 0    # accumulates the payoffs for accepting the innovation
            _payoffquo = 0      # accumulates the payoffs for accepting status quo
            if len(self.neighbors) == 0:
                raise ReferenceError('No neighbors found')
            for n in self.neighbors:
                _s = n.state
                _payoffInnov += _s*(1+alpha)    # alpha boosts the payoff received for accepting the innovation
                _payoffquo   += 1-_s            # following a status quo neighbor gives unit reward
            if _payoffInnov > _payoffquo:    # if _payoffInnov is bigger:
                return 1                     # accept the innovation
            elif _payoffInnov < _payoffquo : # if _payoffquo is bigger:
                return 0                     # revert
            else:                            # if neither is bigger:
                return self.state            # keep the old state
        
        else: # update based on trends
            _zeta_current = zetas[-1]
            _zeta_prev    = zetas[-2]
            if _zeta_current > _zeta_prev:      # if the fraction increased:
                return 1                        # adopt
            elif _zeta_current < _zeta_prev:    # if it decreased:
                return 0                        # revert
            else:                               # if it stayed the same:
                return self.state               # keep the old state

def create_Agents(number: int):
    for _ in range(number):
        _tmp = Agent()

def eval_frac(lst: list) -> float:
    total_adopters = sum(lst)
    return total_adopters/len(lst)

def evaluate_all_neighbors(agent_array: list[Agent], num: int):
    all_agents_copy = agent_array.copy()
    agent: Agent
    for agent in all_agents_copy:
        agent.eval_Neighbors(num_neighbors=num_neighbors)

    agent_array = all_agents_copy

 

def run_sim(iterations: int, plot: bool) -> list[float]:
    global all_agents
    global num_agents

    # initiate the Agents
    all_agents = []
    create_Agents(number=num_agents)

    all_states = [a.state for a in all_agents]
    fraction: int
    fractions_array: list[float] = [0, 0] # the two initial zeros are needed for the update rule that follows the trend.
    reps = 0
    points = []

    for timestep in range(iterations):
        all_states = [a.state for a in all_agents]  # store the states of all agents, and
        fraction = eval_frac(all_states)            # evaluate the fraction of adopters based on all states
        fractions_array.append(fraction)
        points.append(fraction)

        evaluate_all_neighbors(agent_array=all_agents, num=num_neighbors) # re-evaluate the neighbors of each node every timestep (time-varying graph)
        
        new_states = [agent.eval_state(zetas=fractions_array) for agent in all_agents]   # evaluate the next state for each Agent, and store it in a list. Then,
        for agent, state in zip(all_agents, new_states):            # loop throuph the state array and the agent array and
            agent.state = state                                     # update the agents state
        reps += 1

    # plot adoption fraction over time
    if plot:
        plt.figure(figsize=(10,10), num='adoption_curve_game_theoretic')
        plt.plot(np.linspace(1, reps, num=reps), points)
        plt.title(label=f'Output of the Game-Theoretic Model with Parameters alpha = {alpha}, s = {trend_sensitivity} and p = {update_prob}.')
        plt.show()
    
    
    return points

""" set_params(alphaI=5.0, trend_sensitivityI=0.1, seed_fracI=0.1, num_agentsI=500, num_neighborsI=5, update_probI=0.5)
run_sim(iterations=15, plot=True) """