import matplotlib.pyplot as plt
import numpy as np
import random
from icecream import ic


all_agents = []
seed_frac = 0.1 # number of seed agents

alpha = 0.5


class Agent:
    global all_agents
    
    def __init__(self):
        all_agents.append(self)
        self.neighbors = []
        self.state = 0 # 0 -> has not adopted the innovation, 1 -> has adopted the innovation
        if random.random() < seed_frac:
            self.state = 1
    
    def eval_Neighbors(self, num_neighbors: int):
        for _ in range(num_neighbors):
            new_n = random.choice(all_agents)
            while new_n in self.neighbors or new_n == self:
                new_n = random.choice(all_agents)
            self.neighbors.append(new_n)
    
    def eval_state(self):
        if len(self.neighbors) == 0:
           raise ReferenceError('No neighbors found')
        
        interact: Agent = random.choice(self.neighbors)
        if interact.state == 0:
            print('interact neighbor in zero state')
        
        


def create_Agents(number: int):
    for _ in range(number):
        tmp = Agent()

def eval_frac(lst: list) -> float:
    total_adopters = sum(lst)
    return total_adopters/len(lst)

def run_sim():
    global all_agents

    create_Agents(number=10)
    print(all_agents)

run_sim()