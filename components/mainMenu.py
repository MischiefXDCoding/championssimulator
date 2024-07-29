import pygame

class mainMenu:
    def __init__(self, screen):
        self.screen = screen

        # Start Game Button
        startGameButton = pygame.draw.rect(screen, (255, 0, 0), (pygame.display.get_surface().get_size()[0]/2-150, pygame.display.get_surface().get_size()[1]-200, 300, 100), border_radius=10) # x, y, width, height
        displayedStartGameText = pygame.font.Font(None, 36).render('Play Now!', True, (255, 255, 255))
        displayedStartGameTextRect = displayedStartGameText.get_rect(center=(pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-150))
        screen.blit(displayedStartGameText, displayedStartGameTextRect)

        # Settings Button
        settingsButton = pygame.draw.rect(screen, (255, 255, 0), (pygame.display.get_surface().get_size()[0]/2+175, pygame.display.get_surface().get_size()[1]-200, 100, 100), border_radius=10)
        settingsGUICog = pygame.font.Font(None, 36).render('Settings', True, (255, 255, 255))
        displayedSettingsGUICog = settingsGUICog.get_rect(center=(pygame.display.get_surface().get_size()[0]/2+225, pygame.display.get_surface().get_size()[1]-150))
        screen.blit(settingsGUICog, displayedSettingsGUICog)


    def startGame(self):
        #pygame.draw.rect(self.screen, (255, 0, 0), (100, 100, 100, 300)) # x, y, width, height
        pass