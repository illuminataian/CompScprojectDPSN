import pygame
import random
import time
import utils
import titlescreen
from inputs import keyboards, mouse

pygame.init()

# Screen dimensions and setup
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
GEN_X, GEN_Y  = WIDTH /2, HEIGHT/2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AAAAAAAAAAAAAA IM GOING CRAZY")
TIME_LIMIT = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 50)

# Sound effects
correct_sound = pygame.mixer.Sound("media/Sounds/Correct.mp3")
wrong_sound = pygame.mixer.Sound("media/Sounds/Wrong.mp3")

pygame.mixer.music.load("media/Sounds/CompScproject_loop.wav")
pygame.mixer.music.play(-1)

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
    utils.generate_random_key_command(),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 10.0},
    {"type": "mouse", "action": "Right-click", "button": 3, "time_limit": 10.0},
]

current_task = random.choice(commands)
score = 0
is_running = True
start_time = None
timer_started = False

def end_game(final_score):
    #End the game and display the final score.
    wrong_sound.play()
    pygame.mixer.music.stop()
    global is_running
    is_running = False
    print(f"Game Over! Final Score: {final_score}")
    
titlescreen.show_title_screen(screen, font, small_font, WIDTH, HEIGHT)

while is_running:
    
    screen.blit(backgrounds[current_background_index], (0, 0))
    utils.draw_text_with_outline(screen, font, f"{current_task['action']}", (255, 0, 0), WHITE, WIDTH / 2, HEIGHT / 2 )
    utils.draw_text_with_outline(screen, font, f"Score: {score}", (255, 255, 0), (0, 0, 0), WIDTH / 2, HEIGHT / 2 - 100)

    # Start the timer for the current task
    if not timer_started:
        start_time = time.time()
        timer_started = True

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = max(0, current_task.get("time_limit", 0) - elapsed_time)
    utils.draw_text_with_outline(screen, font, f"Time Left: {time_left:.2f}s", GREEN, (0, 0, 0), WIDTH / 2, HEIGHT / 2 + 100)

    # Lose condition (TIME LIMIT)
    if time_left == 0:
        print("Time's up!")
        end_game(score)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            is_running = False

        # Key event handling
        if current_task["type"] == "key":
            if keyboards.handle_keyboard_input(event, current_task["key"]):
                print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                GEN_X, GEN_Y = utils.random_dims(HEIGHT, WIDTH)
                correct_sound.play()
                score, current_task["time_limit"] = utils.update_score(
                    score, current_task.get("time_limit", TIME_LIMIT), difficulty_multiplier=0.9
                )
                update_background()
                current_task = utils.pick_new_command(commands)
                timer_started = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                end_game(score)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse button clicked: {event.button} (Wrong Button)")
                end_game(score)

        # Mouse event handling
        elif current_task["type"] == "mouse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.handle_mouse_input(event, current_task):
                    print(f"Mouse button clicked: {event.button} (Correct)")
                    GEN_X, GEN_Y = utils.random_dims(HEIGHT, WIDTH)
                    correct_sound.play()
                    score, current_task["time_limit"] = utils.update_score(
                        score, current_task.get("time_limit", TIME_LIMIT), difficulty_multiplier=0.9
                    )
                    update_background()
                    current_task = utils.pick_new_command(commands)
                    timer_started = False
                else:
                    print(f"Mouse button clicked: {event.button} (Wrong Button)")
                    end_game(score)
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                end_game(score)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Game over screen
screen.fill(WHITE)
utils.draw_text_with_outline(screen, font, f"Game Over! Final Score: {score}", RED,BLACK, WIDTH // 2, HEIGHT // 2)
pygame.display.flip()
pygame.time.wait(5 * 1000)

pygame.quit()
