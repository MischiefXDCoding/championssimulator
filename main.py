import pygame
from components.MainMenu.mainMenu import loadMenu as loadMainMenu, menuListener as mainMenuListener
from components.MainGame.mainGame import loadGame as loadMainGame, gameListener as mainGameListener, loadGameInformation as loadMainGameInformation


## Base GUI
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Legends Champions League Simulator")
clock = pygame.time.Clock()
running = True
mainmenu = True
maingame = False


gameComponents = {

}



while running:
    backgroundImage = pygame.image.load("mainBackground.png")
    screen.blit(backgroundImage, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if mainmenu:
        loadMainMenu(screen)
        mainmenureturn = mainMenuListener(screen, pygame.mouse.get_pos())
        if mainmenureturn is False:
            mainmenu = False
            maingame = True
            loadMainGameInformation()

    elif maingame:
        loadMainGame(screen)
        maingamereturn = mainGameListener(screen, pygame.mouse.get_pos())
        if maingamereturn is False:
            mainmenu = True
            maingame = False

    else:
        print("ERROR: No menu loaded")
    pygame.display.flip()

    clock.tick(60) 

pygame.quit()