import pygame
import time
import os
import random


class MainGame():
    def __init__(self):
        self.loadingMainUI = True
        self.game = None
        self.returnToMainMenu = None
        self.returnToMainMenuSurface = None
        self.backArrow = None
        self.gameStore = [{ "sixteen-matches": {}, "quarter-matches": {}, "semi-matches": {}, "finals-matches": {}, "quarter-teams": [], "semi-teams": [], "finals-teams": [], "match-types": ["sixteen-matches", "quarter-matches", "semi-matches", "finals-matches"] }]
        self.currentMatchType = "sixteen-matches"
        self.fullRoundLoaded = [False, 0]
        self.output  = {"sixteen-results": {}, "quarter-results": {}, "semi-results": {}, "finals-results": {}}
        self.numberToWord = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
        self.resultsLoading = False
        self.mainMatch = False
        self.matchCount = 0
        self.commentaryFound = False
        self.currEndMatchTypeTime = 0
        self.commentaryCSV = { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }
        self.information = { "clubs": {  }, "commentary": { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }, "players": {} }


    def loadGameInformation(self):
        self.gameStore = [{ "sixteen-matches": {}, "quarter-matches": {}, "semi-matches": {}, "finals-matches": {}, "quarter-teams": [], "semi-teams": [], "finals-teams": [], "match-types": ["sixteen-matches", "quarter-matches", "semi-matches", "finals-matches"] }]
        self.information = { "clubs": {  }, "commentary": { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }, "players": {} }
        for csvFile in os.listdir((os.getcwd()+"\\components\\MainGame\\data")):
            if csvFile.endswith(".csv"):
                with open(os.getcwd()+"\\components\\MainGame\\data\\"+csvFile, 'r') as file:
                    lines = file.readlines()
                    
                    for line in lines:
                        if csvFile[:-4] == "clubs":
                            self.information["clubs"][line.strip()] = { "name": line.strip(), "rating": 0, "players": [] }
                        elif csvFile[:-4] == "commentary":
                            line = [line for line in line.split(",")]
                            self.information["commentary"][line[0]].append(line[1].strip())
                        elif csvFile[:-4] == "players":
                            line = [line for line in line.split(",")]
                            self.information["players"][line[0]] = { "name": line[1], "club": line[0], "rating": line[2] }
                            self.information ["clubs"][line[0]]["players"].append(line[1])
                            self.information["clubs"][line[0]]["rating"] += int(line[2])

        
        allClubs = random.sample(list(self.information['clubs'].keys()), len(list(self.information['clubs'].keys())))
        self.output = {"sixteen-results": {}, "quarter-results": {}, "semi-results": {}, "finals-results": {}}
        self.commentaryCSV = self.information["commentary"]

        while len(allClubs) > 0:
            self.gameStore[0]['sixteen-matches'][allClubs[0]] = allClubs[1]
            allClubs = allClubs[2:]


        self.matchSimulation("sixteen-matches")
        self.matchSimulation("quarter-matches")
        self.matchSimulation("semi-matches")
        self.matchSimulation("finals-matches")

    def loadGame(self, screen):
        if self.loadingMainUI:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            rectWidth = pygame.display.get_surface().get_width() / 1.25
            rectHeight = pygame.display.get_surface().get_height() * 0.9
            rectX = pygame.display.get_surface().get_width() / 2 - rectWidth / 2
            rectY = 700
            self.game = pygame.Rect(rectX, rectY, rectWidth, rectHeight)

            backgroundImage = pygame.image.load("mainBackground.png")
            self.backArrow = pygame.image.load("./components/MainGame/media/baseNames/leftArrow.png")
            self.backArrow = pygame.transform.scale(self.backArrow, (self.backArrow.get_width() / 2, self.backArrow.get_height() / 2))

            target_y = pygame.display.get_surface().get_height() / 2 - pygame.display.get_surface().get_height() * 0.9 / 2
            while self.game.top > target_y:
                screen.blit(backgroundImage, (0, 0))
                self.game.move_ip(0, -5)

                rectSurface = pygame.Surface((rectWidth, rectHeight), pygame.SRCALPHA)
                rectSurface.fill((0, 0, 0, 180))
                screen.blit(rectSurface, self.game.topleft)

                pygame.display.update()
                time.sleep(0.001)

            self.loadingMainUI = False
            self.currentMatchType = "sixteen-matches"
            self.mainMatch = True
            self.loadGame(screen)
        elif self.resultsLoading:
            rectSurface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
            rectSurface.fill((0, 0, 0, (0 if not self.fullRoundLoaded else 180)))
            screen.blit(rectSurface, self.game.topleft)
            self.returnToMainMenu = pygame.Rect(self.game.x, self.game.y, self.game.width / 10, 50)
            self.returnToMainMenuSurface = pygame.Surface((self.returnToMainMenu.width, self.returnToMainMenu.height), pygame.SRCALPHA)
            self.returnToMainMenuSurface.fill((0, 0, 0, 180))
            screen.blit(self.returnToMainMenuSurface, self.returnToMainMenu.topleft)
            screen.blit(self.backArrow, (self.returnToMainMenu.x + self.returnToMainMenu.width / 2 - self.backArrow.get_width() / 2, self.returnToMainMenu.y + self.returnToMainMenu.height / 2 - self.backArrow.get_height() / 2))
            
            logos = self.gameStore[0][self.currentMatchType]
            tourn = pygame.image.load(f'./components/MainGame/media/baseNames/{self.currentMatchType}.png')
            tourn = pygame.transform.scale(tourn, (tourn.get_width() / 4, tourn.get_height() / 4))
            screen.blit(tourn, (self.game.x + self.game.width / 2 - tourn.get_width() / 2, self.game.y + 50))
            

            for count, logo in enumerate(logos):
                club = pygame.Rect(self.game.x+self.game.x/2, self.game.y + ((list(logos.keys()).index(logo)) if logo in list(logos.keys()) else (list(logos.values()).index(logo))+1) * 50+175, 900, 50)
                clubSurface = pygame.Surface((club.width, club.height), pygame.SRCALPHA)
                clubSurface.fill((0, 0, 0, 180))
                if self.currentMatchType == "finals-matches":
                    if logo == self.output["finals-results"][0]["winner"]:
                        clubName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logo}.png")
                        clubTwoName = pygame.image.load(f"./components/MainGame/media/baseNames/{logos[logo]}.png")
                    else:
                        clubName = pygame.image.load(f"./components/MainGame/media/baseNames/{logo}.png")
                        clubTwoName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logos[logo]}.png")
                elif logo not in list(self.gameStore[0][self.gameStore[0]['match-types'][self.gameStore[0]['match-types'].index(self.currentMatchType)+1]].keys()) and logo not in list(self.gameStore[0][self.gameStore[0]['match-types'][self.gameStore[0]['match-types'].index(self.currentMatchType)+1]].values()):
                    clubName = ((pygame.image.load(f"./components/MainGame/media/baseNames/{logo}.png")))
                    clubTwoName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logos[logo]}.png")
                else:
                    clubName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logo}.png")
                    clubTwoName = pygame.image.load(f"./components/MainGame/media/baseNames/{logos[logo]}.png")
                clubName = pygame.transform.scale(clubName, (clubName.get_width() *0.1, clubName.get_height()*0.1))
                clubTwoName = pygame.transform.scale(clubTwoName, (clubTwoName.get_width() *0.1, clubTwoName.get_height()*0.1))
                clubSurface.blit(clubName, (0, -12.5)) 
                clubSurface.blit(clubTwoName, (700, -12.5))
                clubOneScore = pygame.image.load(f"./components/MainGame/media/scores/{self.numberToWord[self.output[self.currentMatchType[:-8]+"-results"][count][logo]]}.png")
                clubTwoScore = pygame.image.load(f"./components/MainGame/media/scores/{self.numberToWord[self.output[self.currentMatchType[:-8]+"-results"][count][logos[logo]]]}.png")
                clubOneScore = pygame.transform.scale(clubOneScore, (clubOneScore.get_width() *0.1, clubOneScore.get_height()*0.1))
                clubTwoScore = pygame.transform.scale(clubTwoScore, (clubTwoScore.get_width() *0.1, clubTwoScore.get_height()*0.1))
                clubSurface.blit(clubOneScore, (clubName.get_width(), 0-clubName.get_height()/4))
                clubSurface.blit(clubTwoScore, (clubSurface.get_width()-clubName.get_width()*2,0-clubName.get_height()/4))
                screen.blit(clubSurface, club.topleft)
                if not self.fullRoundLoaded[0]:
                    pygame.display.update() 
                    time.sleep(1)
                    
            if self.fullRoundLoaded[0] is False:
                self.fullRoundLoaded = [True, time.time()]
                
            if time.time() > self.fullRoundLoaded[1] + 1 and self.currentMatchType != "finals-matches":
                self.fullRoundLoaded = [False, 0]
                self.currentMatchType = self.gameStore[0]['match-types'][self.gameStore[0]['match-types'].index(self.currentMatchType)+1]

            if self.currentMatchType == "finals-matches":
                winnerText = pygame.image.load("./components/MainGame/media/scores/winner.png")
                winnerLogo = pygame.image.load(f"./components/MainGame/media/winnerNames/{self.output["finals-results"][0]["winner"]}.png")

                winnerText = pygame.transform.scale(winnerText, (winnerText.get_width() / 4, winnerText.get_height() / 4))
                winnerLogo = pygame.transform.scale(winnerLogo, (winnerLogo.get_width() / 4, winnerLogo.get_height() / 4))
                
                screen.blit(winnerText, (self.game.x + self.game.width / 2 - winnerText.get_width() / 2, self.game.y + clubSurface.get_height() + 150))
                screen.blit(winnerLogo, (self.game.x + self.game.width / 2 - winnerLogo.get_width() / 2, self.game.y + clubSurface.get_height() + 50 + winnerText.get_height()))

            pygame.display.update() 

        elif self.mainMatch:
            rectSurface = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
            rectSurface.fill((0, 0, 0, (180)))
            screen.blit(rectSurface, self.game.topleft)
            self.returnToMainMenu = pygame.Rect(self.game.x, self.game.y, self.game.width / 10, 50)
            self.returnToMainMenuSurface = pygame.Surface((self.returnToMainMenu.width, self.returnToMainMenu.height), pygame.SRCALPHA)
            self.returnToMainMenuSurface.fill((0, 0, 0, 180))
            screen.blit(self.returnToMainMenuSurface, self.returnToMainMenu.topleft)
            screen.blit(self.backArrow, (self.returnToMainMenu.x + self.returnToMainMenu.width / 2 - self.backArrow.get_width() / 2, self.returnToMainMenu.y + self.returnToMainMenu.height / 2 - self.backArrow.get_height() / 2))

            if not self.commentaryFound:
                if not (self.currEndMatchTypeTime + 4 < time.time()):
                    try:
                        teamOne = pygame.image.load(f"./components/MainGame/media/baseNames/{list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1].keys())[1]}.png")
                        teamOne = pygame.transform.scale(teamOne, (teamOne.get_width() / 4, teamOne.get_height() / 4))
                        teamTwo = pygame.image.load(f"./components/MainGame/media/baseNames/{list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1].keys())[2]}.png")
                        teamTwo = pygame.transform.scale(teamTwo, (teamTwo.get_width() / 4, teamTwo.get_height() / 4))
                        screen.blit(teamOne, (self.game.x + self.game.width / 4 - teamOne.get_width() / 2, self.game.y + 50))
                        screen.blit(teamTwo, (self.game.x + (self.game.width - self.game.width / 4) - teamOne.get_width() / 2, self.game.y + 50))
                        score = pygame.image.load(f"./components/MainGame/media/scores/{self.numberToWord[self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1][list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1].keys())[1]]]}.png")
                        scoreTwo = pygame.image.load(f"./components/MainGame/media/scores/{self.numberToWord[self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1][list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount-1].keys())[2]]]}.png")
                        scoreTwo = pygame.transform.scale(scoreTwo, (scoreTwo.get_width() / 4, scoreTwo.get_height() / 4))
                        score = pygame.transform.scale(score, (score.get_width() / 4, score.get_height() / 4))
                        screen.blit(score, (self.game.x + self.game.width / 4 - score.get_width() / 2, self.game.y + 100))
                        screen.blit(scoreTwo, (self.game.x + (self.game.width - self.game.width / 4) - teamOne.get_width() / 2, self.game.y + 100))
                        return False
                    except KeyError:
                        return False
                if len(self.output[self.currentMatchType[:-8]+'-results']) > self.matchCount:
                    teamOne = pygame.image.load(f"./components/MainGame/media/baseNames/{list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[1]}.png")
                    teamOne = pygame.transform.scale(teamOne, (teamOne.get_width() / 4, teamOne.get_height() / 4))
                    teamTwo = pygame.image.load(f"./components/MainGame/media/baseNames/{list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[2]}.png")
                    teamTwo = pygame.transform.scale(teamTwo, (teamTwo.get_width() / 4, teamTwo.get_height() / 4))
                    screen.blit(teamOne, (self.game.x + self.game.width / 4 - teamOne.get_width() / 2, self.game.y + 50))
                    screen.blit(teamTwo, (self.game.x + (self.game.width - self.game.width / 4) - teamOne.get_width() / 2, self.game.y + 50))
                    
                    totalGoals = self.output[self.currentMatchType[:-8]+'-results'][self.matchCount][list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[1]] + self.output[self.currentMatchType[:-8]+'-results'][self.matchCount][list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[2]]
                    
                    for goal in range(totalGoals):
                        if goal < self.output[self.currentMatchType[:-8]+'-results'][self.matchCount][list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[1]]:
                            team = list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[1]
                        else:
                            team = list(self.output[self.currentMatchType[:-8]+'-results'][self.matchCount].keys())[2]
                        
                        
                        commentary = random.choice(self.commentaryCSV["Scoring"]).replace("[Player Name]", random.choice(self.information["clubs"][team]["players"]))
                        font = pygame.font.Font(None, 30)
                        text = font.render(commentary, True, (255, 255, 255))
                        screen.blit(text, (self.game.x + self.game.width / 2 - text.get_width() / 2, self.game.y + 150 + goal * 40+20))
                        pygame.display.update()
                        time.sleep(2)
                    

                    self.currEndMatchTypeTime = time.time()
                else:
                    if self.currentMatchType == "finals-matches":
                        self.commentaryFound = True
                        self.resultsLoading = True
                        self.currentMatchType = "sixteen-matches"
                    else:
                        self.currentMatchType = self.gameStore[0]['match-types'][self.gameStore[0]['match-types'].index(self.currentMatchType)+1]
                        self.matchCount = 0
                        self.loadGame(screen)
                        return False
                            

            
            


            self.matchCount += 1
        else:
            return False


    def gameListener(self, screen, mousePosition):
        if self.returnToMainMenu.collidepoint(mousePosition):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.returnToMainMenuSurface.fill((192, 192, 192, 50))
            screen.blit(self.returnToMainMenuSurface, self.returnToMainMenu.topleft)
            pygame.display.update()
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.loadingMainUI = True
                self.fullRoundLoaded = [False, 0]
                self.resultsLoading = False
                self.commentaryFound = False
                return False
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

    def matchSimulation(self, matchType):
        if matchType != "sixteen-matches":
            while len(self.gameStore[0][(matchType[:-8]+"-teams")]) > 0:
                self.gameStore[0][matchType][self.gameStore[0][(matchType[:-8]+"-teams")][0]] = self.gameStore[0][(matchType[:-8]+"-teams")][1]
                self.gameStore[0][(matchType[:-8]+"-teams")] = self.gameStore[0][(matchType[:-8]+"-teams")][2:]

        for count, match in enumerate(self.gameStore[0][matchType]):
            winner = random.randint(self.information["clubs"][match]["rating"], self.information["clubs"][self.gameStore[0][matchType][match]]["rating"] + self.information["clubs"][match]["rating"])
            if winner < self.information["clubs"][match]["rating"]:
                winner = match
            else:
                winner = self.gameStore[0][matchType][match]
            
            winnerScore = random.randint(1, 6)
            loserScore = random.randint(0, winnerScore-1)
            self.output[matchType[:-8]+"-results"][count] = { "winner": winner, match: (winnerScore if match == winner else loserScore), (self.gameStore[0][matchType][match]): (winnerScore if self.gameStore[0][matchType][match] == winner else loserScore) }
            self.gameStore[0][self.gameStore[0]['match-types'][self.gameStore[0]['match-types'].index(matchType)+1][:-8]+"-teams"].append(winner) if matchType != "finals-matches" else None

            if matchType == "finals-matches":
                pass