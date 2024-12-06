import pygame
import random

def draw_text(screen, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pick_new_command(commands):
    return random.choice(commands)

def update_score(score, time_limit, difficulty_increment):
    score += 1
    time_limit = max(1, time_limit - difficulty_increment)  # Ensure the time limit doesn't go below 1 second
    return score, time_limit
