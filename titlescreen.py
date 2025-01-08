import pygame
import utils

def show_title_screen(screen, font, small_font, WIDTH, HEIGHT):
    running = True
    while running:
        
        screen.blit(pygame.transform.scale(pygame.image.load("media/backgrounds/blue.png"), (WIDTH, HEIGHT)), (0, 0))

        utils.draw_text_with_outline(screen, font, "DIDDY FREAK OFF PARTY", (255, 225, 0), (0, 0, 0), WIDTH / 2, HEIGHT / 2 - 100)
        utils.draw_text_with_outline(screen, small_font, "Press any key to start", (255, 255, 255), (0, 0, 0), WIDTH / 2, HEIGHT / 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False 

        pygame.display.flip()
        pygame.time.Clock().tick(60)
