import pygame
import random
import time
from inputs import keyboards
from inputs import mouse
from utils import draw_text, pick_new_command, update_score

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA IM GOING CRAZY")

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
]

current_command = random.choice(commands)
score = 0
running = True
start_time = None
reaction_started = False
time_limit = 5  # Seconds allowed to respond
difficulty_increment = 0.1  # Reduces time limit slightly as score increases


def end_game(score):
    global running
    running = False
    print(f"Game Over! Final Score: {score}")


while running:
    screen.fill(WHITE)
    draw_text(screen, font, f"Command: {current_command['action']}", BLACK, 50, 50)
    draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)

    # Reaction time and timeout check
    if not reaction_started:
        start_time = time.time()
        reaction_started = True

    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        print("Time's up!")
        end_game(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            running = False

        if current_command["type"] == "key":
            if keyboards.handle_keyboard_input(event, current_command):
                print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                score, time_limit = update_score(score, time_limit, difficulty_increment)
                current_command = pick_new_command(commands)
                reaction_started = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                end_game(score)

        elif current_command["type"] == "mouse":
            if mouse.handle_mouse_input(event, current_command):
                print(f"Mouse button clicked: {event.button} (Correct)")
                score, time_limit = update_score(score, time_limit, difficulty_increment)
                current_command = pick_new_command(commands)
                reaction_started = False
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
