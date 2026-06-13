import traceback
import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic


thetamin: float = 0.0
thetamax: float = 0.0
seed_frac: float = 0.0
num_agents: int = 0
num_neighbors: int = 0

def set_params(thetaminI, thetamaxI, seed_fracI, num_agentsI, num_neighborsI):
    global thetamin
    global thetamax
    global seed_frac
    global num_agents
    global num_neighbors

    thetamin = thetaminI # for random theta
    thetamax = thetamaxI
    seed_frac = seed_fracI # initial adopters
    num_agents = num_agentsI
    num_neighbors = num_neighborsI


class Agent:
    global all_agents
    def __init__(self):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0
        self.own_theta = random.uniform(thetamin, thetamax)
        # ic(self.own_theta)
        if random.random() < seed_frac:
            self.own_theta = 0
            self.state = 1
    
    def eval_Neighbors(self, num_neighbors: int):
        for _ in range(num_neighbors):
            new_n = random.choice(all_agents)
            while new_n in self.neighbors or new_n == self:
                new_n = random.choice(all_agents)
            self.neighbors.append(new_n)
    
    def eval_state(self):
        state_total = 0

        # ensure that agents cannot go from state 1 to state 0
        if self.state == 1:
            return 1
         
        for n in self.neighbors:
            state_total += n.state
         
        if state_total/len(self.neighbors)>self.own_theta:
            return 1
        else:
            return 0
        
def create_Agents(number: int):
    for _ in range(number):
        tmp = Agent()



def eval_frac(lst: list) -> float:
    total_adopters = sum(lst)
    return total_adopters/len(lst)

spread_counter = 0

def run_sim(iterations: int) -> list[float]:
    global all_agents
    global spread_counter
    global num_agents

    # initiate the Agents
    all_agents = []
    create_Agents(number=num_agents)

    all_agents_copy = all_agents.copy()

    agent: Agent
    for agent in all_agents_copy:
        agent.eval_Neighbors(num_neighbors=num_neighbors)

    all_agents = all_agents_copy


    all_states = [a.state for a in all_agents]
    fraction = 0.5
    reps = 0
    points = []

    for _ in range(iterations):
        if reps > 1000:
            raise RuntimeError('too many iterations')

        all_states = [a.state for a in all_agents]  # store the states of all agents, and
        fraction = eval_frac(all_states)            # evaluate the fraction of adopters based on all states
        points.append(fraction)

        new_states = [agent.eval_state() for agent in all_agents]   # evaluate the next state for each Agent, and store it in a list. Then,
        for agent, state in zip(all_agents, new_states):            #
            agent.state = state
        reps += 1
    """     
    plt.plot(np.linspace(1, reps, num=reps), points)
    plt.title(label=f'neighbors: {num_neighbors}, theta range from {thetamin} to {thetamax}')
    plt.show()
    """  
    if fraction == 0:
        pass
    else:
        spread_counter += 1
    
    return points

'''
set_params(thetaminI=0.1, thetamaxI=0.5, seed_fracI=0.1, num_agentsI=692, num_neighborsI=20)
runs = 10
for _ in range(runs):
    try:
        run_sim()
    except Exception as e:
        print(e)
        pass
    thetamin += 0.01
    thetamax -= 0.01

print('----------------------------------------------------')
print(f'number of agents: {num_agents}')
print(f'number of neighbors: {num_neighbors}')
print(f'seed agent fraction: {seed_frac}')
print(f'fraction of successfull runs: {spread_counter/runs}')
print('----------------------------------------------------')
'''