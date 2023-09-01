import random
import math 

class Environment:
    def __init__(self):
        pass

    def box_muller(self):
        u1 = random.random()
        u2 = random.random()
        z0 = (-2.0 * math.log(u1))**0.5 * math.cos(2.0 * math.pi * u2)
        return z0
    
    def normal(self, mu, sigma):
        return mu + sigma * self.box_muller()
    
    def step(self, action, isSelected):
        # 
        """ NOTE
            doesn't require the action chosen to determine reward only since 
            the agent needs to know if the user liked what the agent choose or not.
            Based on this value, a reward is given if isSelected is true or no
            reward is given if false.
        """
        mean_reward = 0 # default
        if isSelected:
            mean_reward = 1
        # simulate reward movement with a small variance of 0.1 (Not required)
        reward = self.normal(mu= mean_reward, sigma= 0.1)
        return reward