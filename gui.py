import pygame
import sys

pygame.init()
font = pygame.font.SysFont("Arial", 18)
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

cars = {"N": [], "S": [], "E": [], "W": []}

def update_cars(state):
    for i, d in enumerate(["N","S","E","W"]):
        while len(cars[d]) < state[i]:
            cars[d].append(0)

def move_cars(action):
    speed = 2

    for i in range(len(cars["N"])):
        if action == 0:
            cars["N"][i] += speed

    for i in range(len(cars["S"])):
        if action == 0:
            cars["S"][i] += speed

    for i in range(len(cars["E"])):
        if action == 1:
            cars["E"][i] += speed

    for i in range(len(cars["W"])):
        if action == 1:
            cars["W"][i] += speed

    for d in cars:
        cars[d] = [c for c in cars[d] if c < 300]

def draw(state, action):
    screen.fill((0,0,0))

    # roads
    pygame.draw.rect(screen,(50,50,50),(250,0,100,600))
    pygame.draw.rect(screen,(50,50,50),(0,250,600,100))

    # signals
    ns = (0,255,0) if action==0 else (255,0,0)
    ew = (0,255,0) if action==1 else (255,0,0)

    pygame.draw.circle(screen, ns, (300,200), 15)
    pygame.draw.circle(screen, ew, (200,300), 15)

    # cars
    for pos in cars["N"]:
        pygame.draw.circle(screen,(255,255,255),(300,pos),5)

    for pos in cars["S"]:
        pygame.draw.circle(screen,(255,255,255),(300,600-pos),5)

    for pos in cars["E"]:
        pygame.draw.circle(screen,(255,255,255),(600-pos,300),5)

    for pos in cars["W"]:
        pygame.draw.circle(screen,(255,255,255),(pos,300),5)

    # -------- TEXT DISPLAY --------
    total = sum(state)

    text1 = font.render(f"State (N,S,E,W): {state}", True, (255,255,255))
    text2 = font.render(f"Total Vehicles: {total}", True, (255,255,0))
    text3 = font.render(f"Signal: {'NS Green' if action==0 else 'EW Green'}", True, (0,255,0))

    screen.blit(text1, (10,10))
    screen.blit(text2, (10,30))
    screen.blit(text3, (10,50))

    pygame.display.flip()

def run(env, agent):
    state = env.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action = agent.choose_action(state)
        state, _, _ = env.step(action)

        update_cars(state)
        move_cars(action)

        draw(state, action)
        clock.tick(8)