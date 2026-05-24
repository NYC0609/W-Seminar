import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic

all_agents = []
seed_frac = 0.1 # initial adopters
num_agents = 690
num_neighbors = 20


class Agent:
    global all_agents
    def __init__(self, thetamin, thetamax):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0
        self.own_theta = random.uniform(thetamin, thetamax)
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
        will_eval = random.random()
        if will_eval < 0.2: # will stay in old state
            return
        for n in self.neighbors:
            state_total += n.state
        self.state = 1 if state_total/len(self.neighbors)>self.own_theta else 0 # 1 if average of states is greater than theta, 0 else
        

def create_Agents(number: int, thmax: float, thmin: float):
    for _ in range(number):
        tmp = Agent(thetamax=thmax, thetamin=thmin)



def eval_frac(lst: list) -> float:
    total_adopters = sum(lst)
    return total_adopters/len(lst)

spread_counter = 0

def run_sim(agent_numer: int, thetamax: float, thetamin: float, plot: bool) -> list[float]: # returns the fractions of adopters at each timestep
    global all_agents
    global spread_counter



    all_agents = []
    create_Agents(number=agent_numer, thmax=thetamax, thmin=thetamin)

    all_agents_copy = all_agents.copy()

    agent: Agent
    for agent in all_agents_copy:
        agent.eval_Neighbors(num_neighbors=num_neighbors)

    all_agents = all_agents_copy

    all_states = [a.state for a in all_agents]
    fraction = 0.5
    reps = 0
    points = [] # stores the adopter fractions

    while fraction != 1 and fraction !=0:
        if reps > 1000:
            raise RuntimeError('too many iterations')
        all_states = [a.state for a in all_agents]
        fraction = eval_frac(all_states)
        points.append(fraction)

        for agent in all_agents_copy:
            agent.eval_state()
        all_agents = all_agents_copy
        reps += 1
    if plot: 
        plt.plot(np.linspace(1, reps, num=reps), points)
        plt.title(label=f'neighbors: {num_neighbors}, theta range from {thetamin} to {thetamax}')
        plt.show()

   
    if fraction == 0:
        print(0)
        pass
    else:
        print(1)
        spread_counter += 1
    return points

def run_series(number_runs):
    for _ in range(number_runs):
        try:
            run_sim()
        except RuntimeError as e:
            ic(thetamin, thetamax)
            print(e)
        thetamin += 0.01
        thetamax -= 0.01

    print('----------------------------------------------------')
    print(f'number of agents: {num_agents}')
    print(f'number of neighbors: {num_neighbors}')
    print(f'seed agent fraction: {seed_frac}')
    print(f'fraction of successfull runs: {spread_counter/runs}')
    print('----------------------------------------------------')


