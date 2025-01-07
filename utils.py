import pygame
import random
import string

def draw_text(screen, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pick_new_command(commands):
    command = random.choice(commands)
    if command["type"] == "key":
        # Dynamically generate the random key command
        return generate_random_key_command(base_time_limit=3)
    return command

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

def draw_text_with_outline(screen, font, text, text_color, outline_color, center_x, center_y):
    outline_offset = 4
    # Render the main text to get its size
    main_text = font.render(text, True, text_color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    
    # Draw the outline by rendering the text at slightly offset positions
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                outline_rect = outline_text.get_rect(center=(center_x, center_y))
                screen.blit(outline_text, (outline_rect.x + dx, outline_rect.y + dy))
    
    # Draw the main text
    screen.blit(main_text, text_rect)