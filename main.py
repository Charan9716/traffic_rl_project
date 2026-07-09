import matplotlib.pyplot as plt
from environment import TrafficEnv
from q_agent import QAgent
from baseline import fixed_policy

# ================= SETTINGS =================
TRAIN = True        # True → show graph, False → instant GUI
EPISODES = 60       # reduced for faster demo
STEPS = 50

# ================= INIT =================
env = TrafficEnv()
agent = QAgent()

rl_rewards = []
fixed_rewards = []

# ================= TRAINING =================
if TRAIN:
    print("Training started...\n")

    for ep in range(EPISODES):

        state = env.reset()
        total = 0

        for step in range(STEPS):
            action = agent.choose_action(state)
            next_state, reward, _ = env.step(action)

            agent.update(state, action, reward, next_state)

            state = next_state
            total += reward

        rl_rewards.append(total)

        # -------- BASELINE --------
        state = env.reset()
        total = 0
        for step in range(STEPS):
            action = fixed_policy(step)
            state, reward, _ = env.step(action)
            total += reward

        fixed_rewards.append(total)

    print("Training complete!\n")

    # ================= GRAPH =================
    plt.figure()
    plt.plot(rl_rewards, label="RL Agent")
    plt.plot(fixed_rewards, label="Fixed Signal")
    plt.legend()
    plt.title("Traffic Signal Optimization")
    plt.xlabel("Episodes")
    plt.ylabel("Total Reward")
    plt.grid()
    plt.show()

# ================= GUI =================
print("Launching GUI...\n")

from gui import run
run(env, agent)