import pygame
from PIL import Image, ImageFont, ImageDraw

class MainMenu:
    def __init__(self):        
        self.startGameButtonPosition = (0, 0)
        self.startGameButton = None
        self.currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonScaled.png"

    def loadMenu(self, screen):
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
        self.startGameButton = pygame.image.load(self.currentStartGameButtonPath)
        self.startGameButtonPosition = (0.5*pygame.display.get_surface().get_width()-self.startGameButton.get_width()/2, pygame.display.get_surface().get_height()-0.3*pygame.display.get_surface().get_height())
        screen.blit(self.startGameButton, self.startGameButtonPosition)


    def menuListener(self, screen, mousePosition):
        if mousePosition[0] >= self.startGameButtonPosition[0] and mousePosition[0] <= self.startGameButtonPosition[0]+self.startGameButton.get_width() and mousePosition[1] >= self.startGameButtonPosition[1] and mousePosition[1] <= self.startGameButtonPosition[1]+self.startGameButton.get_height():
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

            self.currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonHoverScaled.png"

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                return False
        
            return True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.currentStartGameButtonPath = "./components/MainMenu/MainMenuComponents/startGameButtonScaled.png"
            self.loadMenu(screen)