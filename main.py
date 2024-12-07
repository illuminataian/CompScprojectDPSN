import pygame
import random
import time
import utils
from inputs import keyboards, mouse

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA IM GOING CRAZY")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 50)

# Sound effects
sound_correct = pygame.mixer.Sound("media/Sounds/Correct.mp3")
sound_wrong = pygame.mixer.Sound("media/Sounds/Wrong.mp3")

# Initial commands
commands = [
    utils.generate_random_key_command(base_time_limit=3),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 2},
    {"type": "mouse", "action": "Right-click", "button": 3, "time_limit": 1.5},
]

# Variables
current_command = random.choice(commands)
score = 0
running = True
start_time = None
reaction_started = False
combo_keys = []
combo_index = 0

# Ends the game and prints the score
def end_game(score):
    global running
    running = False
    print(f"Game Over! Final Score: {score}")

# Main game loop
while running:
    screen.fill(WHITE)  # Clear screen

    # Display command and score
    if current_command["type"] == "key" and combo_keys:
        utils.draw_text(screen, font, f"Command: Press {combo_keys[combo_index].upper()}", BLACK, 50, 50)
    else:
        utils.draw_text(screen, font, f"Command: {current_command['action']}", BLACK, 50, 50)
    utils.draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)

    # Start reaction timer
    if not reaction_started:
        start_time = time.time()
        reaction_started = True

    # Display remaining time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, current_command.get("time_limit", 0) - elapsed_time)
    utils.draw_text(screen, font, f"Time Left: {remaining_time:.2f}s", GREEN, 50, 150)

    # Check if time runs out
    if remaining_time == 0:
        print("Time's up!")
        sound_wrong.play()
        end_game(score)

    # Handle events (keyboard/mouse inputs)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            running = False

        if current_command["type"] == "key":  # Key-based commands
            if combo_keys:  # Handle combo sequences
                if keyboards.handle_keyboard_input(event, getattr(pygame, f"K_{combo_keys[combo_index]}")):
                    sound_correct.play()
                    combo_index += 1
                    score += 1
                    start_time = time.time()  # Reset timer for next key
                    if combo_index == len(combo_keys):  # Completed combo
                        combo_keys = []
                        combo_index = 0
                        current_command = utils.pick_new_command(commands + [utils.generate_random_key_command(base_time_limit=3)])
                        reaction_started = False
                elif event.type == pygame.KEYDOWN:  # Wrong key ends game
                    sound_wrong.play()
                    end_game(score)
            else:  # Single key command
                if keyboards.handle_keyboard_input(event, current_command["key"]):
                    sound_correct.play()
                    score += 1
                    score, current_command["time_limit"] = utils.update_score(score, current_command.get("time_limit", 3), difficulty_multiplier=0.9)
                    combo_keys = keyboards.generate_keyboard_input(combo_length=6)  # New combo
                    combo_index = 0
                    start_time = time.time()
                    reaction_started = True

        elif current_command["type"] == "mouse":  # Mouse-based commands
            if mouse.handle_mouse_input(event, current_command):
                sound_correct.play()
                score += 1
                score, current_command["time_limit"] = utils.update_score(score, current_command.get("time_limit", 3), difficulty_multiplier=0.9)
                current_command = utils.pick_new_command(commands + [utils.generate_random_key_command(base_time_limit=3)])
                reaction_started = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Wrong click ends game
                sound_wrong.play()
                end_game(score)

    pygame.display.flip()  # Update screen
    pygame.time.Clock().tick(60)  # Limit to 60 FPS

# Show final score
screen.fill(WHITE)
utils.draw_text(screen, font, f"Game Over! Final Score: {score}", RED, WIDTH // 2 - 200, HEIGHT // 2 - 50)
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
