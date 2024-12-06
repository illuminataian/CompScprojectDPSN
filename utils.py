import pygame
import random
import string

def draw_text(screen, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pick_new_command(commands):
    return random.choice(commands)

def update_score(score, time_limit, difficulty_multiplier):
    score += 1
    time_limit *= difficulty_multiplier
    time_limit = max(time_limit, 0.5) #Set min time to 0.5 sec
    return score, time_limit

def generate_random_key_command(base_time_limit=3):
    random_letter = random.choice(string.ascii_uppercase)
    return {
        "type": "key",
        "action": f"Press {random_letter}",
        "key": getattr(pygame, f"K_{random_letter.lower()}"),
        "time_limit": base_time_limit,
    }
