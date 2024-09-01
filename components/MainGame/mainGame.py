import pygame
import PIL
import time
import os
import json
import random

inMenu = True
loadingMainUI = True
game = None
returnToMainMenu = None
returnToMainMenuSurface = None
backArrow = None
clubImage = None
gameStore = [{ "sixteen-matches": {}, "quarter-matches": {}, "semi-matches": {}, "finals-matches": {}, "quarter-teams": [], "semi-teams": [], "finals-teams": [], "match-types": ["sixteen-matches", "quarter-matches", "semi-matches", "finals-matches"] }]
currentMatchType = "sixteen-matches"
fullRoundLoaded = [False, 0]
output  = {"sixteen-results": {}, "quarter-results": {}, "semi-results": {}, "finals-results": {}}
numberToWord = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
resultsLoading = False
mainMatch = False
matchCount = 0
commentaryFound = False
currEndMatchTypeTime = 0
commentaryCSV = { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }
information = { "clubs": {  }, "commentary": { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }, "players": {} }
totalCommentary = []

def loadGameInformation():
    global gameStore
    global output
    global commentaryCSV
    global information
    gameStore = [{ "sixteen-matches": {}, "quarter-matches": {}, "semi-matches": {}, "finals-matches": {}, "quarter-teams": [], "semi-teams": [], "finals-teams": [], "match-types": ["sixteen-matches", "quarter-matches", "semi-matches", "finals-matches"] }]
    information = { "clubs": {  }, "commentary": { "Attack": [], "Scoring": [], "Defend": [],  "Foul": [], "Penalty": [], "Ref Decision": [], "Man of the Match": [], "Outcome": [] }, "players": {} }
    for csvFile in os.listdir((os.getcwd()+"\\components\\MainGame\\data")):
        if csvFile.endswith(".csv"):
            with open(os.getcwd()+"\\components\\MainGame\\data\\"+csvFile, 'r') as file:
                lines = file.readlines()
                
                for line in lines:
                    if csvFile[:-4] == "clubs":
                        information["clubs"][line.strip()] = { "name": line.strip(), "rating": 0, "players": [] }
                    elif csvFile[:-4] == "commentary":
                        line = [line for line in line.split(",")]
                        information["commentary"][line[0]].append(line[1].strip())
                    elif csvFile[:-4] == "players":
                        line = [line for line in line.split(",")]
                        information["players"][line[0]] = { "name": line[1], "club": line[0], "rating": line[2] }
                        information ["clubs"][line[0]]["players"].append(line[1])
                        information["clubs"][line[0]]["rating"] += int(line[2])

    
    allClubs = random.sample(list(information['clubs'].keys()), len(list(information['clubs'].keys())))
    output = {"sixteen-results": {}, "quarter-results": {}, "semi-results": {}, "finals-results": {}}
    commentaryCSV = information["commentary"]

    while len(allClubs) > 0:
        gameStore[0]['sixteen-matches'][allClubs[0]] = allClubs[1]
        allClubs = allClubs[2:]

    def matchSimulation(matchType):
        if matchType != "sixteen-matches":
            while len(gameStore[0][(matchType[:-8]+"-teams")]) > 0:
                gameStore[0][matchType][gameStore[0][(matchType[:-8]+"-teams")][0]] = gameStore[0][(matchType[:-8]+"-teams")][1]
                gameStore[0][(matchType[:-8]+"-teams")] = gameStore[0][(matchType[:-8]+"-teams")][2:]

        for count, match in enumerate(gameStore[0][matchType]):
            winner = random.randint(information["clubs"][match]["rating"], information["clubs"][gameStore[0][matchType][match]]["rating"] + information["clubs"][match]["rating"])
            if winner < information["clubs"][match]["rating"]:
                winner = match
            else:
                winner = gameStore[0][matchType][match]
            
            winnerScore = random.randint(1, 6)
            loserScore = random.randint(0, winnerScore-1)
            output[matchType[:-8]+"-results"][count] = { "winner": winner, match: (winnerScore if match == winner else loserScore), (gameStore[0][matchType][match]): (winnerScore if gameStore[0][matchType][match] == winner else loserScore) }
            gameStore[0][gameStore[0]['match-types'][gameStore[0]['match-types'].index(matchType)+1][:-8]+"-teams"].append(winner) if matchType != "finals-matches" else None

            if matchType == "finals-matches":
                print("Winner of the Tournament: ", winner)

    matchSimulation("sixteen-matches")
    matchSimulation("quarter-matches")
    matchSimulation("semi-matches")
    matchSimulation("finals-matches")


    with open("output.json", 'w') as file:
        json.dump(output, file, indent=4)

def loadGame(screen):
    global game
    global returnToMainMenuSurface
    global returnToMainMenu
    global backArrow
    global gameStore
    global currentMatchType
    global loadingMainUI
    global fullRoundLoaded
    global numberToWord
    global output
    global resultsLoading
    global mainMatch
    global matchCount
    global commentaryFound
    global currEndMatchTypeTime
    global commentaryCSV    
    global information
    global totalCommentary
    if loadingMainUI:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        rectWidth = pygame.display.get_surface().get_width() / 1.25
        rectHeight = pygame.display.get_surface().get_height() * 0.9
        rectX = pygame.display.get_surface().get_width() / 2 - rectWidth / 2
        rectY = 700
        game = pygame.Rect(rectX, rectY, rectWidth, rectHeight)

        backgroundImage = pygame.image.load("mainBackground.png")
        backArrow = pygame.image.load("./components/MainGame/media/baseNames/leftArrow.png")
        backArrow = pygame.transform.scale(backArrow, (backArrow.get_width() / 2, backArrow.get_height() / 2))

        target_y = pygame.display.get_surface().get_height() / 2 - pygame.display.get_surface().get_height() * 0.9 / 2
        while game.top > target_y:
            screen.blit(backgroundImage, (0, 0))
            game.move_ip(0, -5)

            rectSurface = pygame.Surface((rectWidth, rectHeight), pygame.SRCALPHA)
            rectSurface.fill((0, 0, 0, 180))
            screen.blit(rectSurface, game.topleft)

            pygame.display.update()
            time.sleep(0.001)

        loadingMainUI = False
        currentMatchType = "sixteen-matches"
        mainMatch = True
        loadGame(screen)
    elif resultsLoading:
        rectSurface = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
        rectSurface.fill((0, 0, 0, (0 if not fullRoundLoaded else 180)))
        screen.blit(rectSurface, game.topleft)
        returnToMainMenu = pygame.Rect(game.x, game.y, game.width / 10, 50)
        returnToMainMenuSurface = pygame.Surface((returnToMainMenu.width, returnToMainMenu.height), pygame.SRCALPHA)
        returnToMainMenuSurface.fill((0, 0, 0, 180))
        screen.blit(returnToMainMenuSurface, returnToMainMenu.topleft)
        screen.blit(backArrow, (returnToMainMenu.x + returnToMainMenu.width / 2 - backArrow.get_width() / 2, returnToMainMenu.y + returnToMainMenu.height / 2 - backArrow.get_height() / 2))
        
        logos = gameStore[0][currentMatchType]
        tourn = pygame.image.load(f'./components/MainGame/media/baseNames/{currentMatchType}.png')
        tourn = pygame.transform.scale(tourn, (tourn.get_width() / 4, tourn.get_height() / 4))
        screen.blit(tourn, (game.x + game.width / 2 - tourn.get_width() / 2, game.y + 50))
        

        for count, logo in enumerate(logos):
            club = pygame.Rect(game.x+game.x/2, game.y + ((list(logos.keys()).index(logo)) if logo in list(logos.keys()) else (list(logos.values()).index(logo))+1) * 50+175, 900, 50)
            clubSurface = pygame.Surface((club.width, club.height), pygame.SRCALPHA)
            clubSurface.fill((0, 0, 0, 180))
            if currentMatchType == "finals-matches":
                if logo == output["finals-results"][0]["winner"]:
                    clubName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logo}.png")
                    clubTwoName = pygame.image.load(f"./components/MainGame/media/baseNames/{logos[logo]}.png")
                else:
                    clubName = pygame.image.load(f"./components/MainGame/media/baseNames/{logo}.png")
                    clubTwoName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logos[logo]}.png")
            elif logo not in list(gameStore[0][gameStore[0]['match-types'][gameStore[0]['match-types'].index(currentMatchType)+1]].keys()) and logo not in list(gameStore[0][gameStore[0]['match-types'][gameStore[0]['match-types'].index(currentMatchType)+1]].values()):
                clubName = ((pygame.image.load(f"./components/MainGame/media/baseNames/{logo}.png")))
                clubTwoName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logos[logo]}.png")
            else:
                clubName = pygame.image.load(f"./components/MainGame/media/winnerNames/{logo}.png")
                clubTwoName = pygame.image.load(f"./components/MainGame/media/baseNames/{logos[logo]}.png")
            clubName = pygame.transform.scale(clubName, (clubName.get_width() *0.1, clubName.get_height()*0.1))
            clubTwoName = pygame.transform.scale(clubTwoName, (clubTwoName.get_width() *0.1, clubTwoName.get_height()*0.1))
            clubSurface.blit(clubName, (0, -12.5)) 
            clubSurface.blit(clubTwoName, (700, -12.5))
            clubOneScore = pygame.image.load(f"./components/MainGame/media/scores/{numberToWord[output[currentMatchType[:-8]+"-results"][count][logo]]}.png")
            clubTwoScore = pygame.image.load(f"./components/MainGame/media/scores/{numberToWord[output[currentMatchType[:-8]+"-results"][count][logos[logo]]]}.png")
            clubOneScore = pygame.transform.scale(clubOneScore, (clubOneScore.get_width() *0.1, clubOneScore.get_height()*0.1))
            clubTwoScore = pygame.transform.scale(clubTwoScore, (clubTwoScore.get_width() *0.1, clubTwoScore.get_height()*0.1))
            clubSurface.blit(clubOneScore, (clubName.get_width(), 0-clubName.get_height()/4))
            clubSurface.blit(clubTwoScore, (clubSurface.get_width()-clubName.get_width()*2,0-clubName.get_height()/4))
            screen.blit(clubSurface, club.topleft)
            if not fullRoundLoaded[0]:
                pygame.display.update() 
                time.sleep(1)
                
        if fullRoundLoaded[0] is False:
            fullRoundLoaded = [True, time.time()]
            
        if time.time() > fullRoundLoaded[1] + 1 and currentMatchType != "finals-matches":
            fullRoundLoaded = [False, 0]
            currentMatchType = gameStore[0]['match-types'][gameStore[0]['match-types'].index(currentMatchType)+1]

        if currentMatchType == "finals-matches":
            winnerText = pygame.image.load("./components/MainGame/media/scores/winner.png")
            winnerLogo = pygame.image.load(f"./components/MainGame/media/winnerNames/{output["finals-results"][0]["winner"]}.png")

            winnerText = pygame.transform.scale(winnerText, (winnerText.get_width() / 4, winnerText.get_height() / 4))
            winnerLogo = pygame.transform.scale(winnerLogo, (winnerLogo.get_width() / 4, winnerLogo.get_height() / 4))
            
            screen.blit(winnerText, (game.x + game.width / 2 - winnerText.get_width() / 2, game.y + clubSurface.get_height() + 150))
            screen.blit(winnerLogo, (game.x + game.width / 2 - winnerLogo.get_width() / 2, game.y + clubSurface.get_height() + 50 + winnerText.get_height()))

        pygame.display.update() 

    elif mainMatch:
        rectSurface = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
        rectSurface.fill((0, 0, 0, (180)))
        screen.blit(rectSurface, game.topleft)
        returnToMainMenu = pygame.Rect(game.x, game.y, game.width / 10, 50)
        returnToMainMenuSurface = pygame.Surface((returnToMainMenu.width, returnToMainMenu.height), pygame.SRCALPHA)
        returnToMainMenuSurface.fill((0, 0, 0, 180))
        screen.blit(returnToMainMenuSurface, returnToMainMenu.topleft)
        screen.blit(backArrow, (returnToMainMenu.x + returnToMainMenu.width / 2 - backArrow.get_width() / 2, returnToMainMenu.y + returnToMainMenu.height / 2 - backArrow.get_height() / 2))

        if not commentaryFound:
            if not (currEndMatchTypeTime + 2 < time.time()):
                try:
                    teamOne = pygame.image.load(f"./components/MainGame/media/baseNames/{list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]}.png")
                    teamOne = pygame.transform.scale(teamOne, (teamOne.get_width() / 4, teamOne.get_height() / 4))
                    teamTwo = pygame.image.load(f"./components/MainGame/media/baseNames/{list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[2]}.png")
                    teamTwo = pygame.transform.scale(teamTwo, (teamTwo.get_width() / 4, teamTwo.get_height() / 4))
                    screen.blit(teamOne, (game.x + game.width / 4 - teamOne.get_width() / 2, game.y + 50))
                    screen.blit(teamTwo, (game.x + (game.width - game.width / 4) - teamOne.get_width() / 2, game.y + 50))
                    """font = pygame.font.Font(None, 40)
                    scoreOne = font.render(str(output[currentMatchType[:-8]+'-results'][matchCount][list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]]), True, (255, 255, 255))
                    screen.blit(scoreOne, (game.x + game.width / 2 - scoreOne.get_width() / 2, game.y + 50 + teamOne.get_height() + 10))
                    scoreTwo = font.render(str(output[currentMatchType[:-8]+'-results'][matchCount][list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[2]]), True, (255, 255, 255))
                    screen.blit(scoreTwo, (game.x + game.width / 2 - scoreTwo.get_width() / 2, game.y + 50 + teamOne.get_height() + 10 + scoreOne.get_height() + 10))"""
                    return False
                except KeyError:
                    return False
            if len(output[currentMatchType[:-8]+'-results']) > matchCount:
                teamOne = pygame.image.load(f"./components/MainGame/media/baseNames/{list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]}.png")
                teamOne = pygame.transform.scale(teamOne, (teamOne.get_width() / 4, teamOne.get_height() / 4))
                teamTwo = pygame.image.load(f"./components/MainGame/media/baseNames/{list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[2]}.png")
                teamTwo = pygame.transform.scale(teamTwo, (teamTwo.get_width() / 4, teamTwo.get_height() / 4))
                screen.blit(teamOne, (game.x + game.width / 4 - teamOne.get_width() / 2, game.y + 50))
                screen.blit(teamTwo, (game.x + (game.width - game.width / 4) - teamOne.get_width() / 2, game.y + 50))
                
                totalGoals = output[currentMatchType[:-8]+'-results'][matchCount][list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]] + output[currentMatchType[:-8]+'-results'][matchCount][list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[2]]
                
                for goal in range(totalGoals):
                    if goal < output[currentMatchType[:-8]+'-results'][matchCount][list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]]:
                        team = list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[1]
                    else:
                        team = list(output[currentMatchType[:-8]+'-results'][matchCount].keys())[2]
                    
                    
                    commentary = random.choice(commentaryCSV["Scoring"]).replace("[Player Name]", random.choice(information["clubs"][team]["players"]))
                    font = pygame.font.Font(None, 30)
                    text = font.render(commentary, True, (255, 255, 255))
                    screen.blit(text, (game.x + game.width / 2 - text.get_width() / 2, game.y + 150 + goal * 40+20))
                    pygame.display.update()
                    time.sleep(1) 
                

                print(output)
                currEndMatchTypeTime = time.time()
            else:
                if currentMatchType == "finals-matches":
                    commentaryFound = True
                    resultsLoading = True
                    currentMatchType = "sixteen-matches"
                else:
                    currentMatchType = gameStore[0]['match-types'][gameStore[0]['match-types'].index(currentMatchType)+1]
                    print(currentMatchType)
                    matchCount = 0
                    loadGame(screen)
                    return False
                        

        
        


        matchCount += 1


        """
        LOOP THROUGH OUTPUT JSON
        DO COMMENTARY DEPENDENT ON NUMBER OF GOALS SCORED AND THE HAVE A CERT. PERCENTAGE OF FAILED GOAL WHERE USE DEFENCE COMMENTARY AND ADD ONE TO THE TOTAL GOAL TO MAKE ANOTHER GOAL HAPPEN :D
        """
    else:
        return False


def gameListener(screen, mousePosition):
    global returnToMainMenu
    global returnToMainMenuSurface
    global loadingMainUI
    global fullRoundLoaded
    global commentaryFound
    global resultsLoading
    if returnToMainMenu.collidepoint(mousePosition):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        returnToMainMenuSurface.fill((192, 192, 192, 50))
        screen.blit(returnToMainMenuSurface, returnToMainMenu.topleft)
        pygame.display.update()
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            loadingMainUI = True
            fullRoundLoaded = [False, 0]
            resultsLoading = False
            commentaryFound = False
            return False
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 