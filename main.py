import pygame
import random
import time
import utils
from inputs import keyboards, mouse

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AAAAAAAAAAAAAA IM GOING CRAZY")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)

# Sound effects
correct_sound = pygame.mixer.Sound("media/Sounds/Correct.mp3")
wrong_sound = pygame.mixer.Sound("media/Sounds/Wrong.mp3")

# Commands and initial setup
commands = [
    utils.generate_random_key_command(base_time_limit=3),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 2},
    {"type": "mouse", "action": "Right-click", "button": 3, "time_limit": 1.5},
]

current_task = random.choice(commands)
score = 0
is_running = True
start_time = None
timer_started = False

combo_keys = []
combo_index = 0


def end_game(final_score):
    global is_running
    is_running = False
    print(f"Game Over! Final Score: {final_score}")


while is_running:
    screen.fill(WHITE)

    # Display the current task
    if current_task["type"] == "key" and combo_keys:
        utils.draw_text(
            screen,
            font,
            f"Command: Press {combo_keys[combo_index].upper()}",
            BLACK,
            50,
            50,
        )
    else:
        utils.draw_text(screen, font, f"Command: {current_task['action']}", BLACK, 50, 50)
    utils.draw_text(screen, font, f"Score: {score}", BLACK, 50, 100)

    # Start the timer for the current task
    if not timer_started:
        start_time = time.time()
        timer_started = True

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = max(0, current_task.get("time_limit", 0) - elapsed_time)
    utils.draw_text(screen, font, f"Time Left: {time_left:.2f}s", GREEN, 50, 150)

    # End game if time runs out
    if time_left == 0:
        print("Time's up!")
        wrong_sound.play()
        end_game(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            is_running = False

        if current_task["type"] == "key":
            if combo_keys:
                if keyboards.handle_keyboard_input(event, getattr(pygame, f"K_{combo_keys[combo_index]}")):
                    print(f"Key pressed: {combo_keys[combo_index].upper()} (Correct)")
                    correct_sound.play()
                    combo_index += 1
                    score += 1
                    start_time = time.time()

                    # Move to the next task if the combo is complete
                    if combo_index == len(combo_keys):
                        print("Combo completed!")
                        combo_keys = []
                        combo_index = 0
                        current_task = utils.pick_new_command(
                            commands + [utils.generate_random_key_command(base_time_limit=3)]
                        )
                        timer_started = False
                elif event.type == pygame.KEYDOWN:
                    print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                    wrong_sound.play()
                    end_game(score)
            else:
                if keyboards.handle_keyboard_input(event, current_task["key"]):
                    print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                    correct_sound.play()
                    score += 1
                    score, current_task["time_limit"] = utils.update_score(
                        score, current_task.get("time_limit", 3), difficulty_multiplier=0.9
                    )
                    combo_keys = keyboards.generate_keyboard_input(combo_length=6)
                    combo_index = 0
                    start_time = time.time()
                    timer_started = True

        elif current_task["type"] == "mouse":
            if mouse.handle_mouse_input(event, current_task):
                print(f"Mouse button clicked: {event.button} (Correct)")
                correct_sound.play()
                score += 1
                score, current_task["time_limit"] = utils.update_score(
                    score, current_task.get("time_limit", 3), difficulty_multiplier=0.9
                )
                current_task = utils.pick_new_command(
                    commands + [utils.generate_random_key_command(base_time_limit=3)]
                )
                timer_started = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse button clicked: {event.button} (Wrong Button)")
                wrong_sound.play()
                end_game(score)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Game over screen
screen.fill(WHITE)
utils.draw_text(screen, font, f"Game Over! Final Score: {score}", RED, WIDTH // 2 - 200, HEIGHT // 2 - 50)
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
