import pygame
from components.MainMenu.mainMenu import MainMenu #loadMenu as loadMainMenu, menuListener as mainMenuListener
from components.MainGame.mainGame import MainGame  # as loadMainGame, gameListener as mainGameListener, loadGameInformation as loadMainGameInformation


## Base GUI
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Legends Champions League Simulator")
clock = pygame.time.Clock()
running = True
mainmenu = True
maingame = False
MainMenu = MainMenu()
MainGame = MainGame()

gameComponents = {

}



while running:
    backgroundImage = pygame.image.load("mainBackground.png")
    screen.blit(backgroundImage, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if mainmenu:
        MainMenu.loadMenu(screen = screen)
        mainmenureturn = MainMenu.menuListener(screen, pygame.mouse.get_pos())
        if mainmenureturn is False:
            mainmenu = False
            maingame = True
            MainGame.loadGameInformation()

    elif maingame:
        MainGame.loadGame(screen)
        maingamereturn = MainGame.gameListener(screen = screen, mousePosition = pygame.mouse.get_pos())
        if maingamereturn is False:
            mainmenu = True
            maingame = False

    else:
        print("ERROR: No menu loaded")
        running = False
    pygame.display.flip()

    clock.tick(60) 

pygame.quit()