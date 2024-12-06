import pygame
import random
import time
import utils
from inputs import keyboards
from inputs import mouse

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA IM GOING CRAZY")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)

# Sound effects
sound_correct = pygame.mixer.Sound("media/Sounds/Correct.mp3")
sound_wrong = pygame.mixer.Sound("media/Sounds/Wrong.mp3")

# Commands and initial setup
commands = [
    utils.generate_random_key_command(base_time_limit=3),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 2},
    {"type": "mouse", "action": "Right-click", "button": 3, "time_limit": 1.5},
]

current_command = random.choice(commands)
score = 0
running = True
start_time = None
reaction_started = False

combo_keys = []
combo_index = 0


def end_game(score):
    global running
    running = False
    print(f"Game Over! Final Score: {score}")


while running:
    screen.fill(WHITE)
    if current_command["type"] == "key" and combo_keys:
        utils.draw_text(
            screen,
            font,
            f"Command: Press {combo_keys[combo_index].upper()}",
            BLACK,
            50,
            50,
        )
    else:
        utils.draw_text(screen, font, f"Command: {current_command['action']}", BLACK, 50, 50)

    utils.draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)
    utils.draw_text(
        screen, font, f"Time Left: {current_command.get('time_limit', 0):.2f}s", GREEN, 50, 150
    )

    if not reaction_started:
        start_time = time.time()
        reaction_started = True

    elapsed_time = time.time() - start_time
    if elapsed_time > current_command.get("time_limit", 0):
        print("Time's up!")
        sound_wrong.play()
        end_game(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            running = False

        if current_command["type"] == "key":
            if combo_keys:
                if keyboards.handle_keyboard_input(event, getattr(pygame, f"K_{combo_keys[combo_index]}")):
                    print(f"Key pressed: {combo_keys[combo_index].upper()} (Correct)")
                    sound_correct.play()
                    combo_index += 1
                    score += 1
                    start_time = time.time()
                    reaction_started = True

                    if combo_index == len(combo_keys):  # Combo completed
                        print("Combo completed!")
                        combo_keys = []
                        combo_index = 0
                        current_command = utils.pick_new_command(
                            commands + [utils.generate_random_key_command(base_time_limit=3)]
                        )
                        reaction_started = False
                elif event.type == pygame.KEYDOWN:
                    print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                    sound_wrong.play()
                    end_game(score)
            else:
                if keyboards.handle_keyboard_input(event, current_command["key"]):
                    print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                    sound_correct.play()
                    score += 1
                    score, current_command["time_limit"] = utils.update_score(
                        score, current_command.get("time_limit", 3), difficulty_multiplier=0.9
                    )

                    combo_keys = keyboards.generate_keyboard_input(combo_length=6)
                    combo_index = 0
                    start_time = time.time()
                    reaction_started = True

        elif current_command["type"] == "mouse":
            if mouse.handle_mouse_input(event, current_command):
                print(f"Mouse button clicked: {event.button} (Correct)")
                sound_correct.play()
                score += 1
                score, current_command["time_limit"] = utils.update_score(
                    score, current_command.get("time_limit", 3), difficulty_multiplier=0.9
                )
                current_command = utils.pick_new_command(
                    commands + [utils.generate_random_key_command(base_time_limit=3)]
                )
                reaction_started = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse button clicked: {event.button} (Wrong Button)")
                sound_wrong.play()
                end_game(score)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

screen.fill(WHITE)
utils.draw_text(screen, font, f"Game Over! Final Score: {score}", RED, WIDTH // 2 - 200, HEIGHT // 2 - 50)
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()

