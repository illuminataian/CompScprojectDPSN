import pygame
import random
from inputs import keyboards
from inputs import mouse
from utils import draw_text, pick_new_command

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fun Input Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

def end_game(score):
    global running
    running = False
    print(f"Game Over! Final Score: {score}")

while running:
    screen.fill(WHITE)
    draw_text(screen, font, f"Command: {current_command['action']}", BLACK, 50, 50)
    draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            running = False

        if current_command["type"] == "key":
            if keyboards.handle_keyboard_input(event, current_command):
                print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                score += 1
                current_command = pick_new_command(commands)
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                end_game(score)

        elif current_command["type"] == "mouse":
            if mouse.handle_mouse_input(event, current_command):
                print(f"Mouse button clicked: {event.button} (Correct)")
                score += 1
                current_command = pick_new_command(commands)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse button clicked: {event.button} (Wrong Button)")
                end_game(score)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

screen.fill(WHITE)
draw_text(screen, font, f"Game Over! Final Score: {score}", RED, WIDTH // 2 - 200, HEIGHT // 2 - 50)
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
