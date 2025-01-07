import pygame
import random
import time
import utils
from inputs import keyboards, mouse

pygame.init()

# Screen dimensions and setup
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT),)
pygame.display.set_caption("AAAAAAAAAAAAAA IM GOING CRAZY")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 100)

# Sound effects
correct_sound = pygame.mixer.Sound("media/Sounds/Correct.mp3")
wrong_sound = pygame.mixer.Sound("media/Sounds/Wrong.mp3")

# Backgrounds
backgrounds = [
    pygame.transform.scale(pygame.image.load("media/backgrounds/yellow.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("media/backgrounds/red.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("media/backgrounds/green.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("media/backgrounds/purple.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("media/backgrounds/blue.png"), (WIDTH, HEIGHT)),
       
]
current_background_index = 0

def update_background():
    global current_background_index
    current_background_index = (current_background_index + 1) % len(backgrounds)

# Commands and initial setup
commands = [
    utils.generate_random_key_command(base_time_limit=3),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 1.5},
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
    screen.blit(backgrounds[current_background_index], (0, 0))

    # Display the current task
    if current_task["type"] == "key" and combo_keys:
        utils.draw_text_with_outline(
            screen,
            font,
            f"Command: Press {combo_keys[combo_index].upper()}",
            (255,0,0),
            BLACK,
            WIDTH/2, 
            HEIGHT/2,
        )
    else:
        utils.draw_text_with_outline(screen, font, f"Command: {current_task['action']}", (255, 0, 0), BLACK, WIDTH/2, HEIGHT/2)
        
    utils.draw_text_with_outline(screen, font, f"Score: {score}", (255, 255, 0), (0, 0, 0), WIDTH/2, HEIGHT/2-100)

    # Start the timer for the current task
    if not timer_started:
        start_time = time.time()
        timer_started = True

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = max(0, current_task.get("time_limit", 0) - elapsed_time)
    utils.draw_text_with_outline(screen, font, f"Time Left: {time_left:.2f}s", GREEN,(0, 0, 0), WIDTH/2, HEIGHT/2+100)

    # Lose condition (TIME LIMIT)
    if time_left == 0:
        print("Time's up!")
        wrong_sound.play()
        end_game(score)

    # Game quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            is_running = False

        # Key event handling
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

                        update_background()

                        # Pick a new task
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

                    if not combo_keys:
                        update_background()

                    
        elif current_task["type"] == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.handle_mouse_input(event, current_task):
                    print(f"Mouse button clicked: {event.button} (Correct)")
                    correct_sound.play()
                    score, current_task["time_limit"] = utils.update_score(
                        score, current_task.get("time_limit", 3), difficulty_multiplier=0.9
                    )
                    update_background()
                    current_task = utils.pick_new_command(
                        commands + [utils.generate_random_key_command(base_time_limit=3)]
                    )
                    timer_started = False
                else:
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
