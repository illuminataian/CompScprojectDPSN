import pygame
import time
import random

def start_reaction(screen, command, reaction_started, start_time):
    if not reaction_started:
        if start_time is None:
            start_time = time.time()
        if time.time() - start_time > random.uniform(1, 3):  # Random delay
            screen.fill(command["color"])
            reaction_started = True
            start_time = time.time()  # Start timing player reaction
    return reaction_started, start_time

def handle_reaction_input(event, reaction_started, start_time):
    if reaction_started and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
        elapsed_time = time.time() - start_time
        if elapsed_time < 0.5:
            return True
    return False
