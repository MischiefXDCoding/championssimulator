import pygame
import components.mainMenu as mainMenu


## Base GUI
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


gameComponents = {

}



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            print(event.pos)
            print(pygame.display.get_surface().get_size())

    mainMenu.mainMenu(screen)
        

    pygame.display.flip()

    clock.tick(60) 

pygame.quit()