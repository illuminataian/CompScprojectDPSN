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
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("AAAAAAAAAAAAAA IM GOING CRAZY")
TIME_LIMIT = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

RECT = None

# Fonts
title_Font=pygame.font.Font('media/Fonts/Ethnocentric Rg.otf',170)
font = pygame.font.Font('media/Fonts/Orbitron-Black.ttf', 90)
font_supporting = pygame.font.Font('media/Fonts/Orbitron-Black.ttf', 60)
# Sound effects
correct_sound = pygame.mixer.Sound("media/Sounds/Correct.wav")
wrong_sound = pygame.mixer.Sound("media/Sounds/Wrong.wav")
correct_sound.set_volume(0.1)
wrong_sound.set_volume(0.3)


bgs = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (255, 0, 255), (0, 0, 255)]
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
    utils.generate_random_key_command(base_time_limit=TIME_LIMIT),
    {"type": "mouse", "action": "Left-click", "button": 1, "time_limit": 10.0},
    {"type": "mouse", "action": "Right-click", "button": 3, "time_limit": 10.0},
]

current_task = random.choice(commands)
score = 0
is_running = True
start_time = None
timer_started = False
game_end = False

def end_game(final_score):
    #End the game and display the final score.
    global game_end
    game_end = True
    global timer_started
    timer_started = False
    wrong_sound.play()
    pygame.mixer.music.stop()
    print(f"Game Over! Final Score: {final_score}")
    
titlescreen.show_title_screen(screen, title_Font, WIDTH, HEIGHT)

pygame.mixer.music.load("media/Sounds/CompScproject_loop.wav")
pygame.mixer.music.play(-1)
 
while is_running:
    if not game_end:
        screen.blit(backgrounds[current_background_index], (0, 0))
        utils.draw_text_with_outline(screen, font_supporting, f"Score: {score}", (255, 255, 0), (0, 0, 0), WIDTH / 8, HEIGHT / 12)
        RECT = utils.draw_rect(screen, font, f"{current_task['action']}", (255, 0, 0), WHITE, GEN_X, GEN_Y, bgs[current_background_index])
        # Start the timer for the current task
        if not timer_started:
            start_time = time.time()
            timer_started = True

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        time_left = max(0, current_task.get("time_limit", 0) - elapsed_time)
        utils.draw_text_with_outline(screen, font_supporting, f"Time Left: {time_left:.2f}s", GREEN, (0, 0, 0), WIDTH - WIDTH / 5, HEIGHT - HEIGHT / 12)

        # Lose condition (TIME LIMIT)
        if time_left == 0:
            print("Time's up!")
            end_game(score)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game quit.")
                is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Game quit.")
                is_running = False
            # Keyboard event handling
            if current_task["type"] == "key":
                if keyboards.handle_keyboard_input(event, current_task["key"]):
                    print(f"Key pressed: {pygame.key.name(event.key)} (Correct)")
                    current_task = utils.pick_new_command(commands, time_limit=current_task['time_limit'])
                    
                    correct_sound.play()
                    score, current_task["time_limit"] = utils.update_score(
                        score, current_task['time_limit'], difficulty_multiplier=0.95
                    )
                    update_background()
                    if current_task["type"] == "key":
                        GEN_X, GEN_Y = WIDTH / 2 , HEIGHT /2
                    else:
                        GEN_X, GEN_Y = utils.random_dims( HEIGHT, WIDTH)
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
                    if mouse.handle_mouse_input(event, current_task,):
                        mouse_pos = pygame.mouse.get_pos()
                        if RECT.collidepoint(mouse_pos):
                            print(f"Mouse button clicked: {event.button} (Correct)")
                            GEN_X, GEN_Y = utils.random_dims(HEIGHT, WIDTH)
                            current_task = utils.pick_new_command(commands, time_limit=current_task['time_limit'])
                            correct_sound.play()
                            score, current_task["time_limit"] = utils.update_score(
                                score, current_task.get("time_limit", current_task['time_limit']), difficulty_multiplier=0.95
                            )
                            update_background()
                            if current_task["type"] == "key":
                                GEN_X, GEN_Y = WIDTH / 2 , HEIGHT /2
                            else:
                                GEN_X, GEN_Y = utils.random_dims(HEIGHT, WIDTH)
                            timer_started = False
                        else:
                            print(f"Mouse button clicked: {event.button} (Wrong Button)")
                            end_game(score)
                    else:
                            print(f"Mouse button clicked: {event.button} (Wrong Button)")
                            end_game(score)
                elif event.type == pygame.KEYDOWN:
                    print(f"Key pressed: {pygame.key.name(event.key)} (Wrong Key)")
                    end_game(score)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    else: 
        endtime = 0
        while game_end:
            screen.blit(pygame.transform.scale(pygame.image.load("media/backgrounds/blue.png"), (WIDTH, HEIGHT)), (0, 0))
            utils.draw_text_with_outline(screen, font, f"Game Over! Final Score: {score}", RED,BLACK, WIDTH // 2, HEIGHT // 2 - 100)
            rect = utils.draw_rect(screen, font, f"Play Again", RED,BLACK, WIDTH // 2, HEIGHT // 2 + 100, (0, 255, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_end = False
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_end = False
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if rect.collidepoint(mouse_pos):
                        current_task['time_limit'] = 10
                        score = 0
                        game_end = False
                        is_running = True
                        pygame.mixer.music.load("media/Sounds/CompScproject_loop.wav")
                        pygame.mixer.music.play(-1)
            if endtime >= 150:
                game_end = False
                exit()     
            endtime+=1
            pygame.display.flip()
            pygame.time.Clock().tick(60)



pygame.quit()

