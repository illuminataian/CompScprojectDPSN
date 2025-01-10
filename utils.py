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
        return generate_random_key_command(base_time_limit=20)
    return command

def update_score(score, time_limit, difficulty_multiplier):
    score += 1
    time_limit *= difficulty_multiplier
    time_limit = max(time_limit, 0.5) #Set min time to 0.5 sec
    return score, time_limit

def generate_random_key_command(base_time_limit=20):
    random_letter = random.choice(string.ascii_uppercase)
    return {
        "type": "key",
        "action": f"Press {random_letter}",
        "key": getattr(pygame, f"K_{random_letter.lower()}"),
        "time_limit": base_time_limit,
    }

def draw_text_with_outline(screen, font, text, text_color, outline_color, center_x, center_y):
    outline_offset = 2
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

def draw_rect(screen, font, text, text_color, outline_color, center_x, center_y):
    print(center_x, center_y)
    main_text = font.render(text, True, text_color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20,20))
    outline_offset = 2
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                outline_rect = outline_text.get_rect(center=(center_x, center_y))
                screen.blit(outline_text, (outline_rect.x + dx, outline_rect.y + dy))
    screen.blit(main_text, text_rect)


def random_dims(HEIGHT, WIDTH):
    GEN_X, GEN_Y = random.randint(0 + 100, WIDTH - 100), random.randint(0 + 100, HEIGHT - 100)
    return GEN_X, GEN_Y

def draw_text_gradient(screen, font, text, gradient_colors, glow_color, outline_color, center_x, center_y, outline_offset=2):
    fontglow=pygame.font.Font('media/Fonts/Ethnocentric Rg.otf', 120)
    
    #Render Glow
    '''
    temp_surface = pygame.Surface((fontglow.size(text)[0], fontglow.size(text)[1]), pygame.SRCALPHA)
    glow_surface = fontglow.render(text, True, glow_color)
    temp_surface.blit(glow_surface, (0, 0))
    temp_surface.set_alpha(128)
    glow_rect = temp_surface.get_rect(center=(center_x-5, center_y+10))
    screen.blit(temp_surface, glow_rect)
    '''
    # Render the main text with gradient
    text_surface = pygame.Surface((font.size(text)[0], font.size(text)[1]), pygame.SRCALPHA)
    width, height = text_surface.get_size()

    # Create the gradient on a blank surface
    for y in range(height):
        interpolated_color = [
            gradient_colors[0][i] + (gradient_colors[1][i] - gradient_colors[0][i]) * y // height
            for i in range(3)
        ]
        pygame.draw.line(text_surface, interpolated_color, (0, y), (width, y))

    # Render the text on top of the gradient surface
    text_rendered = font.render(text, True, (255, 255, 255))  # White for blending
    text_surface.blit(text_rendered, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    
    #Draw Glow
    for dx in range(-outline_offset-9, outline_offset + 10, 4):
        for dy in range(-outline_offset-9, outline_offset + 10, 4):
            # Skip the center to avoid double-rendering
            if dx != 0 or dy != 0:
                temp_surface = pygame.Surface((font.size(text)[0], font.size(text)[1]), pygame.SRCALPHA)
                glow_surface = font.render(text, True, glow_color)
                temp_surface.blit(glow_surface, (0, 0))
                temp_surface.set_alpha(15)
                glow_rect = temp_surface.get_rect(center=(center_x + dx, center_y + dy))
                screen.blit(temp_surface, glow_rect)
    
    # Draw the outline
    for dx in range(-outline_offset, outline_offset + 1):
        for dy in range(-outline_offset, outline_offset + 1):
            # Skip the center to avoid double-rendering
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(center_x + dx, center_y + dy))
                screen.blit(outline_surface, outline_rect)

    # Draw the main gradient-filled text
    
    screen.blit(text_surface, text_rect)
