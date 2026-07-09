import numpy as np
import random

class QAgent:
    def __init__(self):
        self.Q = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

    def get_q(self, state):
        if state not in self.Q:
            self.Q[state] = [0,0]
        return self.Q[state]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0,1])
        return int(np.argmax(self.get_q(state)))

    def update(self, s,a,r,s2):
        q = self.get_q(s)
        next_q = self.get_q(s2)
        q[a] += self.alpha * (r + self.gamma*max(next_q) - q[a])