import pygame
import random
import string
import math

def draw_text(screen, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pick_new_command(commands, time_limit):
    print(time_limit)
    index = math.floor(random.random() * 3) + 1
    print(index)
    if index > 1:
        command = commands[0]
    else:
        command = random.choice(commands[1:])
    if command["type"] == "key":
        # Dynamically generate the random key command
        return generate_random_key_command(base_time_limit=time_limit)
    else:
        command['time_limit'] = time_limit
        return command

def update_score(score, time_limit, difficulty_multiplier):
    score += 1
    time_limit *= difficulty_multiplier
    time_limit = max(time_limit, 0.5) #Set min time to 0.5 sec
    return score, time_limit

def generate_random_key_command(base_time_limit):
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


def draw_button(screen, font, text, text_color, outline_color, center_x, center_y, color):
    main_text = font.render(text, True, text_color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    s = pygame.Surface(text_rect.inflate(60,60).size)
    s.set_alpha(30)
    s.fill((255, 255, 255))
    screen.blit(s, (text_rect.inflate(60,60).left, text_rect.inflate(60,60).top))
    pygame.draw.rect(s, pygame.color.Color(255, 255, 255, 100), text_rect.inflate(60,60))
    for i in range(10):
        pygame.draw.rect(screen, color, text_rect.inflate(60 - i, 60 - i), 1)
    outline_offset = 2
    # Render the main text to get its size
    main_text = font.render(text, True, color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    
    # Draw the outline by rendering the text at slightly offset positions
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, (0, 0, 0))
                outline_rect = outline_text.get_rect(center=(center_x, center_y))
                screen.blit(outline_text, (outline_rect.x + dx, outline_rect.y + dy))

    # Draw the main text
    screen.blit(main_text, text_rect)
    return text_rect.inflate(60, 60)

def draw_rect(screen, font, text, text_color, outline_color, center_x, center_y, color):
    main_text = font.render(text, True, text_color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    s = pygame.Surface(text_rect.inflate(60,60).size)
    s.set_alpha(30)
    s.fill((255, 255, 255))
    screen.blit(s, (text_rect.inflate(60,60).left, text_rect.inflate(60,60).top))
    pygame.draw.rect(s, pygame.color.Color(255, 255, 255, 100), text_rect.inflate(60,60))
    for i in range(10):
        pygame.draw.rect(screen, color, text_rect.inflate(60 - i, 60 - i), 1)
    outline_offset = 2
    # Render the main text to get its size
    main_text = font.render(text, True, color)
    text_rect = main_text.get_rect(center=(center_x, center_y))
    
    # Draw the outline by rendering the text at slightly offset positions
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, (0, 0, 0))
                outline_rect = outline_text.get_rect(center=(center_x, center_y))
                screen.blit(outline_text, (outline_rect.x + dx, outline_rect.y + dy))

    # Draw the main text
    screen.blit(main_text, text_rect)
    return text_rect.inflate(60, 60)


def random_dims(HEIGHT, WIDTH):
    GEN_X, GEN_Y = random.randint(0 + 300, WIDTH - 300), random.randint(0 + 200, HEIGHT - 200)
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
