import pygame
from PIL import Image, ImageFont, ImageDraw
startGameButtonPosition = (0, 0)
startGameButton = None
currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonScaled.png"

def loadMenu(screen):
    global startGameButtonPosition
    global startGameButton
    global currentStartGameButtonPath
    with Image.open("./components/MainMenu/MainMenuComponents/startGameButton.png") as startGameButtonImage:
        
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
        
        newStartGameButtonImage.save("./components/MainMenu/MainMenuComponents/startGameButtonScaled.png")
    startGameButton = pygame.image.load(currentStartGameButtonPath)
    startGameButtonPosition = (0.5*pygame.display.get_surface().get_width()-startGameButton.get_width()/2, pygame.display.get_surface().get_height()-0.3*pygame.display.get_surface().get_height())
    screen.blit(startGameButton, startGameButtonPosition)


def menuListener(screen, mousePosition):
    global startGameButton
    global startGameButtonPosition
    global currentStartGameButtonPath

    if mousePosition[0] >= startGameButtonPosition[0] and mousePosition[0] <= startGameButtonPosition[0]+startGameButton.get_width() and mousePosition[1] >= startGameButtonPosition[1] and mousePosition[1] <= startGameButtonPosition[1]+startGameButton.get_height():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        with Image.open("./components/MainMenu/MainMenuComponents/startGameButtonHover.png") as startGameButtonImage:
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
            
            newStartGameButtonImage.save("./components/MainMenu/MainMenuComponents/startGameButtonHoverScaled.png")

        currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonHoverScaled.png"

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            return False
    
        return True
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonScaled.png"
        loadMenu(screen)