import random
import pygame

def generate_random_key_command():
    """Generate a random key command."""
    random_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
    return {
        "type": "key",
        "action": f"Press {random_letter.upper()}",
        "key": getattr(pygame, f"K_{random_letter}"),
        "time_limit": 20,
    }

def handle_keyboard_input(event, expected_key):
    """Check if the correct key is pressed."""
    return event.type == pygame.KEYDOWN and event.key == expected_key