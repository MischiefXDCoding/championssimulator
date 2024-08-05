import pygame
from PIL import Image, ImageFont, ImageDraw
startGameButtonPosition = (0, 0)
startGameButton = None
currentStartGameButtonPath = "./components/MainMenu/startGameButtonScaled.png"

def loadMenu(screen):
    global startGameButtonPosition
    global startGameButton
    global currentStartGameButtonPath
    print("Ran load menu.")
    with Image.open("./components/MainMenu/startGameButton.png") as startGameButtonImage:
        
        screen_width, screen_height = pygame.display.get_surface().get_size()
        maxWidth = screen_width * 0.3
        maxHeight = screen_height * 0.25

        aspectRatio = startGameButtonImage.width / startGameButtonImage.height
        if startGameButtonImage.width > startGameButtonImage.height:
            newWidth = min(maxWidth, startGameButtonImage.width)
            newHeight = newWidth / aspectRatio
        else:
            newHeight = min(maxHeight, startGameButtonImage.height)
            newWidth = newHeight * aspectRatio

        newStartGameButtonImage = startGameButtonImage.resize((int(newWidth), int(newHeight)), Image.LANCZOS)
        
        newStartGameButtonImage.save("./components/MainMenu/startGameButtonScaled.png")
    startGameButton = pygame.image.load(currentStartGameButtonPath)
    startGameButtonPosition = (0.5*pygame.display.get_surface().get_width()-startGameButton.get_width()/2, pygame.display.get_surface().get_height()-0.3*pygame.display.get_surface().get_height())
    screen.blit(startGameButton, startGameButtonPosition)
    print(startGameButton)
    print(startGameButtonPosition)


def startGame():
    #pygame.draw.rect(screen, (255, 0, 0), (100, 100, 100, 300)) # x, y, width, height
    pass


def menuListener(screen, mousePosition):
    global startGameButton
    global startGameButtonPosition
    global currentStartGameButtonPath
    print(startGameButton)
    print(startGameButtonPosition)
    
    #print(mousePosition)
    #print(startGameButtonPosition
    if mousePosition[0] >= startGameButtonPosition[0] and mousePosition[0] <= startGameButtonPosition[0]+startGameButton.get_width() and mousePosition[1] >= startGameButtonPosition[1] and mousePosition[1] <= startGameButtonPosition[1]+startGameButton.get_height():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        with Image.open("./components/MainMenu/startGameButtonHover.png") as startGameButtonImage:
            screen_width, screen_height = pygame.display.get_surface().get_size()
            maxWidth = screen_width * 0.3
            maxHeight = screen_height * 0.25

            aspectRatio = startGameButtonImage.width / startGameButtonImage.height
            if startGameButtonImage.width > startGameButtonImage.height:
                newWidth = min(maxWidth, startGameButtonImage.width)
                newHeight = newWidth / aspectRatio
            else:
                newHeight = min(maxHeight, startGameButtonImage.height)
                newWidth = newHeight * aspectRatio

            newStartGameButtonImage = startGameButtonImage.resize((int(newWidth), int(newHeight)), Image.LANCZOS)
            
            newStartGameButtonImage.save("./components/MainMenu/startGameButtonHoverScaled.png")

        currentStartGameButtonPath = "./components/MainMenu/startGameButtonHoverScaled.png"

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            pygame.quit()
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        currentStartGameButtonPath = "./components/MainMenu/startGameButtonScaled.png"