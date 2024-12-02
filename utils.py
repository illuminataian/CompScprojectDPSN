import pygame
import random

def draw_text(screen, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def pick_new_command(commands):
    return random.choice(commands)
