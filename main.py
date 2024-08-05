import pygame
from components.MainMenu.mainMenu import loadMenu as loadMainMenu, menuListener as mainMenuListener



## Base GUI
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Legends Champions League Simulator")
clock = pygame.time.Clock()
running = [True, False]
mainmenu = True


gameComponents = {

}


while running[0]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255,0,0))
    loadMainMenu(screen)
    if mainmenu:
        mainMenuListener(screen, pygame.mouse.get_pos())

    pygame.display.flip()

    clock.tick(60) 

pygame.quit()