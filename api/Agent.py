import math
import random

# BASE CLASS
class Agent:
    def __init__(self, k=4):
        self.actions = ["Tech","News","Health","Money"]
        self.k = k 
        self.epsilon = 0.35
        self.alpha = 0.1 
        
    def clear(self):
        pass
    
    def initialize_zeros(self):
        return [0 for _ in range(self.k)]   

    def decay_epsilon(self):
        self.epsilon = max(0.15, self.epsilon * 0.95)

    def decay_alpha(self):
        self.alpha = max(0.1, self.alpha * 0.995)   

# AGENTS    
class UCB_AGENT(Agent):
    def __init__(self, k=4):
        super().__init__(k)
        self.Q = self.initialize_zeros()
        self.k_counts = self.initialize_zeros()
        self.selection_states = ['','','','']

    # UCB
    def choose_action(self, c=1):
        total_counts = sum(self.k_counts)

        # if no counts, return some random action
        if total_counts == 0:
            return int(math.floor(random.random() * self.k))
        
        ucb_values = [0] * self.k
        for a in range(self.k):
            exploitation_term = self.Q[a]
            # Added epsilon to avoid division by zero
            exploration_term = math.sqrt(math.log(total_counts)/(float(self.k_counts[a]) + 1e-5))
            explore_confidence = c * exploration_term
            # variable to see if we are exploring or exploiting
            self.isExploring[a] = 'Exploration' if explore_confidence > exploitation_term else 'Exploitation'
            
            ucb_values[a] = exploitation_term + explore_confidence

        action = ucb_values.index(max(ucb_values))
        
        # increment count
        self.increment_action_count()

        return action
    
    def increment_action_count(self, action):
        self.k_counts[action] += 1

    def learn(self, action, reward):
        # convert action text to index
        action_index = self.actions.index(action)
        # get action count
        count = self.k_counts[action_index]
        # IA equation
        self.Q[action_index] = self.Q[action_index] + ((reward - self.Q[action_index])/count)

        return self.Q.copy(), self.isExploring

class GBA_AGENT(Agent):
    def __init__(self, k=4):
        super().__init__(k)
        self.H = self.initialize_zeros() # track preferences (grows infinitely positive/negative)
        self.pi = self.initialize_zeros() # track probabilities
        self.avg_reward = 0 # track avg reward
        self.total_rewards = 0 # track total rewards (grows infinitely)
        self.t = 0  # track current time-step (grows infinitely)
        self.selection_state = ''   

    # softmax
    def choose_action(self):
        # get exponentiation array of H 
        exp_h = [math.exp(self.H[i]) for i in range(self.k)]
        # get pi (probabilities)
        self.pi =  [exp_h[i] / sum(exp_h) for i in range(self.k)] 
        # get action - exploration or exploitation
        action = random.choices(range(len(self.pi)), self.pi)[0]
        # Update selection state so we can see back on web app
        self.selection_state = 'Exploration' if self.pi[action] < max(self.pi) else 'Exploitation'

        return action
    
    def learn(self, action, reward):
        # convert action text to index
        action_index = self.actions.index(action)
        # increment time-step
        self.t += 1 
        # update total rewards with current
        self.total_rewards += reward
        # update avg reward
        self.avg_reward += (reward - self.avg_reward) / self.t
        # update preferences
        for a in range(self.k):
            # current action chosen
            if a == action_index:
                self.H[a] += self.alpha * (reward - self.avg_reward) * (1 - self.pi[a])
            # other actions
            else:
                self.H[a] -= self.alpha * (reward - self.avg_reward) * self.pi[a]
        
        # decay
        self.decay_alpha()

        return self.H.copy()

class ERWA_AGENT (Agent):
    def __init__(self, k=4):
        super().__init__(k)
        self.Q = self.initialize_zeros()
        self.selection_state = ''

    def clear(self):
        self.Q = self.initialize_zeros()
        self.selection_state = ''

    # e-greedy
    def choose_action(self):
        if random.random() < self.epsilon:
            self.selection_state = 'Exploration'
            return random.choice(range(self.k))
        else:
            self.selection_state = 'Exploitation'
            return self.Q.index(max(self.Q))

    def learn(self, action, reward):
        # convert action text to index
        action_index = self.actions.index(action)
        # ERWA simplified equation
        self.Q[action_index] = (1 - self.alpha) * self.Q[action_index] + (reward * self.alpha)
        # decay - removed
        # self.decay_epsilon()
        # self.decay_alpha()

        return self.Q.copy()
    
