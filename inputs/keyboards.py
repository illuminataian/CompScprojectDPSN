import pygame
def handle_keyboard_input(event, command):
    if event.type == pygame.KEYDOWN and event.key == command["key"]:
        return True
    return False
