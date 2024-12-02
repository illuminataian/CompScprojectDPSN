import pygame
import random
from inputs import keyboards
from inputs import mouse
from inputs import reaction
from utils import draw_text, pick_new_command


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fun Input Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 50)

commands = [
    {"type": "key", "action": "Press A", "key": pygame.K_a},
    {"type": "key", "action": "Press Space", "key": pygame.K_SPACE},
    {"type": "mouse", "action": "Left-click", "button": 1},
    {"type": "mouse", "action": "Right-click", "button": 3},
    {"type": "reaction", "action": "Wait for Green!", "color": GREEN},
]
current_command = random.choice(commands)
score = 0
running = True
start_time = None
reaction_started = False

while running:
    screen.fill(WHITE)
    draw_text(screen, font, f"Command: {current_command['action']}", BLACK, 50, 50)
    draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)

    if current_command["type"] == "reaction":
        reaction_started, start_time = reaction.start_reaction(
            screen, current_command, reaction_started, start_time
        )

# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_command["type"] == "key":
            if keyboards.handle_keyboard_input(event, current_command):
                score += 1
                current_command = pick_new_command(commands)

        elif current_command["type"] == "mouse":
            if mouse.handle_mouse_input(event, current_command):
                score += 1
                current_command = pick_new_command(commands)

        elif current_command["type"] == "reaction":
            result = reaction.handle_reaction_input(event, reaction_started, start_time)
            if result:
                score += 1
                current_command = pick_new_command(commands)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
