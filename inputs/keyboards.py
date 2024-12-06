import random
import pygame
# Define keyboard sections
keyboard_sections = {
    "section_1": ["q", "w", "e", "a", "s", "d", "z", "x", "c"],
    "section_2": ["r", "t", "y", "f", "g", "h", "v", "b", "n"],
    "section_3": ["u", "i", "o", "j", "k", "l", "m", "p"]
}

def generate_keyboard_input(section_name, combo_length=6):
    section = keyboard_sections.get(section_name, [])
    if len(section) < combo_length:
        raise ValueError(f"Section '{section_name}' does not have enough keys for a combo.")
    return random.sample(section, combo_length)

def handle_keyboard_input(event, expected_key):
    if event.type == pygame.KEYDOWN and event.key == expected_key:
        return True
    return False