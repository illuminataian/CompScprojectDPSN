import pygame

def handle_mouse_input(event, command):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == command["button"]:
        return True
    return False
