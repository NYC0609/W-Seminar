import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic

all_agents = []
num_agents = 690
num_neighbors = 4


class Agent:
    global all_agents
    def __init__(self, thetamin, thetamax, seed_frac):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0
        self.own_theta = random.uniform(thetamin, thetamax) # the lower the theta value, the easier the agent adopts the innovation
        if random.random() < seed_frac:
            self.own_theta = 0
            self.state = 1
    
    def eval_Neighbors(self, num_neighbors: int):
        for _ in range(num_neighbors):
            new_n = random.choice(all_agents)
            while new_n in self.neighbors or new_n == self:
                new_n = random.choice(all_agents)
            self.neighbors.append(new_n)
    
    def eval_state(self) -> int:
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


def create_Agents(number: int, thmax: float, thmin: float, seed_frac: float):
    for _ in range(number):
        tmp = Agent(thetamax=thmax, thetamin=thmin, seed_frac=seed_frac)



def eval_frac(lst: list) -> float:
    total_adopters = sum(lst)
    return total_adopters/len(lst)

spread_counter = 0

def run_sim(agent_numer: int, thetamax: float, thetamin: float, seed_frac: float, iterations: int, plot: bool) -> list[float]: # returns the fractions of adopters at each timestep
    global all_agents
    global spread_counter



    all_agents = []
    create_Agents(number=agent_numer, thmax=thetamax, thmin=thetamin, seed_frac=seed_frac)

    all_agents_copy = all_agents.copy()

    agent: Agent
    for agent in all_agents_copy:
        agent.eval_Neighbors(num_neighbors=num_neighbors)

    all_agents = all_agents_copy

    all_states = [a.state for a in all_agents]
    fraction = 0.5
    points = [] # stores the adopter fractions

    for _ in range(iterations):
        all_states = [a.state for a in all_agents]
        fraction = eval_frac(all_states)
        points.append(fraction)

        new_states: list[int] = []
        for agent in all_agents:
            new_states.append(agent.eval_state())

        for id, state in enumerate(new_states):
            all_agents[id].state = state

        # print(fraction)

    if plot: 
        plt.plot(np.linspace(1, iterations, num=iterations), points)
        plt.title(label=f'neighbors: {num_neighbors}, theta range from {thetamin} to {thetamax}')
        plt.show()
    return points


run_sim(agent_numer=50, thetamax=0.4, thetamin=0.1, iterations=20, seed_frac=0.1, plot=False)

