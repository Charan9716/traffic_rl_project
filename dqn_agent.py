import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4,32),
            nn.ReLU(),
            nn.Linear(32,2)
        )

    def forward(self,x):
        return self.net(x)

class DQNAgent:
    def __init__(self):
        self.model = DQN()
        self.target = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.memory = deque(maxlen=1000)
        self.gamma = 0.9
        self.epsilon = 0.1

    def choose_action(self,state):
        if random.random() < self.epsilon:
            return random.choice([0,1])
        state = torch.FloatTensor(state)
        return torch.argmax(self.model(state)).item()

    def store(self,s,a,r,s2):
        self.memory.append((s,a,r,s2))

    def train(self):
        if len(self.memory) < 32:
            return

        batch = random.sample(self.memory,32)

        for s,a,r,s2 in batch:
            s = torch.FloatTensor(s)
            s2 = torch.FloatTensor(s2)

            q = self.model(s)[a]
            target = r + self.gamma*torch.max(self.target(s2))

            loss = (q - target.detach())**2

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()