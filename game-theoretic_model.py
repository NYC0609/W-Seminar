import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic


all_agents = []
seed_frac = 0.1 # number of seed agents

def set_params(alphaI, seed_fracI, num_agentsI, num_neighborsI):
    global alpha
    global seed_frac
    global num_agents
    global num_neighbors

    alpha = alphaI
    seed_frac = seed_fracI # initial adopters
    num_agents = num_agentsI
    num_neighbors = num_neighborsI

class Agent:
    global all_agents
    
    def __init__(self):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0 # 0 -> has not adopted the nnovation, 1 -> has adopted the innovation
        if random.random() < seed_frac:
            self.state = 1
            print('seed node')
    
    def eval_Neighbors(self, num_neighbors: int):
        self.neighbors = []
        for _ in range(num_neighbors):
            new_n = random.choice(all_agents)
            while new_n in self.neighbors or new_n == self:
                new_n = random.choice(all_agents)
            self.neighbors.append(new_n)
    
    def eval_state(self):
        _payoffInnov = 0    # accumulates the payoffs for accepting the innovation
        _payoffquo = 0      # accumulates the payoffs for accepting status quo
        if len(self.neighbors) == 0:
           raise ReferenceError('No neighbors found')
        for n in self.neighbors:
            _s = n.state
            _payoffInnov += _s*(1+alpha)    # alpha boosts the payoff received for accepting the innovation
            _payoffquo   += 1-_s            # following a status quo neighbor gives unit reward
        #print('payoff for 1:', _payoffInnov)
        #print('payoff for 0:', _payoffquo)

        if _payoffInnov > _payoffquo:   # if _payoffInnov is bigger,
            return 1                    # accept the innovation
        elif _payoffquo > _payoffInnov: # if _payoffquo is bigger,
            return 0                    # go to status quo
        else:                           # if neither is bigger,
            return self.state           # keep the old state
        
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
    global spread_counter
    global num_agents

    # initiate the Agents
    all_agents = []
    create_Agents(number=num_agents)

    all_states = [a.state for a in all_agents]
    fraction = 0.5
    reps = 0
    points = []

    for timestep in range(iterations):
        print(f'starting timestep {timestep}')

        all_states = [a.state for a in all_agents]  # store the states of all agents, and
        print('all states:', all_states)
        fraction = eval_frac(all_states)            # evaluate the fraction of adopters based on all states
        points.append(fraction)

        evaluate_all_neighbors(agent_array=all_agents, num=num_neighbors) # re-evaluate the neighbors of each node every timestep (time-varying graph)
        
        new_states = [agent.eval_state() for agent in all_agents]   # evaluate the next state for each Agent, and store it in a list. Then,
        for agent, state in zip(all_agents, new_states):            # loop throuph the state array and the agent array and
            agent.state = state                                     # update the agents state
        reps += 1

        # end the loop if the fraction reaches either 0 or 1
        if fraction == 0:
            break
        elif fraction == 1:
            break

    # plot adoption fraction over time
    if plot:
        plt.figure(figsize=(10,10), num='adoption_curve_game_theoretic')
        plt.plot(np.linspace(1, reps, num=reps), points)
        plt.title(label=f'neighbors: {num_neighbors}, alpha value {alpha}')
        plt.show()
    
    
    return points

set_params(alphaI=5, seed_fracI=0.1, num_agentsI=500, num_neighborsI=10)
run_sim(iterations=100, plot=True)