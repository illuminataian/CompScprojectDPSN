import pygame
import utils
import math

def show_title_screen(screen, font, WIDTH, HEIGHT):
    running = True
    offset=0
    gradient_colors = [(255, 255, 0), (255, 165, 0)]  # Yellow to Orange gradient
    glow_color = (255, 255, 150)  # Pale Yellow Glow
    outline_color = (0, 0, 0)  # Black Outline

    while running:
        small_font = pygame.font.Font('media/Fonts/Orbitron-Bold.ttf',int(46 + (2*math.sin(offset*3))))
        screen.blit(pygame.transform.scale(pygame.image.load("media/backgrounds/blue.png"), (WIDTH, HEIGHT)), (0, 0))

       # utils.draw_text_with_outline(screen, font, "IMPULSE", (255, 225, 0), (0, 0, 0), WIDTH / 2, HEIGHT / 2 - 100 + (5*math.sin(offset))) {+ (10*math.sin(offset))}
        utils.draw_text_with_outline(screen, small_font, "Press any key to start", (255, 255, 255), (0, 0, 0), WIDTH / 2, HEIGHT / 2 + 100)
        offset+=0.3
        utils.draw_text_gradient(screen, font, "IMPULSE", gradient_colors, glow_color, outline_color, WIDTH // 2, HEIGHT // 2 - 100 + (5*math.sin(offset)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False 

        pygame.display.flip()
        pygame.time.Clock().tick(60)

