import random

class TrafficEnv:
    def __init__(self):
        self.state = [0,0,0,0]

    def reset(self):
        self.state = [random.randint(0,5) for _ in range(4)]
        return tuple(self.state)

    def step(self, action):
        # new cars arrive
        for i in range(4):
            self.state[i] += random.randint(0,2)

        # cars pass
        if action == 0:
            self.state[0] = max(0, self.state[0]-3)
            self.state[1] = max(0, self.state[1]-3)
        else:
            self.state[2] = max(0, self.state[2]-3)
            self.state[3] = max(0, self.state[3]-3)

        queue = sum(self.state)
        reward = -queue

        return tuple(self.state), reward, queue