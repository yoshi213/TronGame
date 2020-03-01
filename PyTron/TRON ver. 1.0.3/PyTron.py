import pygame
import time
from GameBoard import GameBoard
from MainMenu import MainMenu
from Match import Match
from Player import Player, Human, Computer
from SelectColorMenu import SelectColorMenu #Add SelectColorMenu Class


class Game:
    # Create game class
    def __init__(self, xTiles, yTiles, tileSize):
        # Start pygame
        pygame.init()
        pygame.display.set_caption('PyTron')

        # Set board size
        self.xTiles = xTiles
        self.yTiles = yTiles
        self.tileSize = tileSize

        # Set window size
        self.scr_x = tileSize * xTiles
        self.scr_y = tileSize * yTiles
        self.screen = pygame.display.set_mode((self.scr_x, self.scr_y))

        self.state = None  # state machine for different game states
        self.board = GameBoard(self, xTiles, yTiles, tileSize)  # Build game board
        self.mainMenu = MainMenu(self)
        self.match = None
        self.players = {}  # playerId is the key
        self.selectColorMenu = SelectColorMenu(self)    #make instance

        # Initialize stats values
        self.PVE_PlayerWins = 0
        self.PVE_BotWins = 0
        self.PVE_Tie = 0
        self.PVP_Player1Wins = 0
        self.PVP_Player2Wins = 0
        self.PVP_Tie = 0
        self.EVE_Bot1Wins = 0
        self.EVE_Bot2Wins = 0
        self.EVE_Tie = 0

        # Start initally at main menu
        self.switchToMainMenu()





    def eventLoop(self):
        # Set clock and playing state
        clock = pygame.time.Clock()
        playing = True

        # Start program loop
        while playing:
            # Handle events per program state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                if self.state == 'START_MENU':
                    self.mainMenu.eventTick(event)
                elif self.state == 'Select_COLOR_MENU':
                    self.selectColorMenu.eventTick(event)
                elif self.state == 'PLAYING_MATCH':
                    self.match.event(event)
                elif self.state == 'GAME_OVER':
                    self.gameOverMenu.event(event)




            # game logic and drawing
            if self.state == 'START_MENU':
                pass
            elif self.state == 'Select_COLOR_MENU': #Add this statement to contorol program  well
                pass
            elif self.state == 'PLAYING_MATCH':
                self.match.tick()


            pygame.display.flip()
            if self.state == 'PLAYING_MATCH':
                clock.tick(10)  # low fps for slow movement
            else:
                clock.tick(60)  # Otherwise high fps for menus
        # Quit when done playing
        pygame.quit()
        quit()

    # Draw main menu and set program state
    def switchToMainMenu(self):
        self.mainMenu.draw()
        self.state = 'START_MENU'

    # Draw game over screen and set program state
    def switchToGameOver(self):
        self.gameOverMenu.draw()
        self.state = 'GAME_OVER'

    #Add this method to control program well
    def switchSelectColorMenu(self):
        self.selectColorMenu.draw()
        self.state = 'Select_COLOR_MENU'

    def startMatch(self, matchType):
        print("Starting match. Type:", matchType)
        self.board = GameBoard(self, self.xTiles, self.yTiles, self.tileSize)
        self.players = {}
        # Create players/Computers per match type.

        # PVP - 2 humans
        if matchType == 0:
            self.players[1] = Human(self, self.selectColorMenu.getP1Color(), 1, 3, 3, Player.DIRECT_RIGHT,
                                    (pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_LSHIFT))
            self.players[2] = Human(self, self.selectColorMenu.getP2Color(), 2, self.board.xTiles - 4,
                                    self.board.yTiles - 4, Player.DIRECT_LEFT,
                                    (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RSHIFT))
        # PVE - 1 human and 1 bot
        elif matchType == 1:
            self.players[1] = Human(self, self.selectColorMenu.getP1Color(), 1, 3, 3, Player.DIRECT_RIGHT,
                                    (pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_LSHIFT))
            self.players[2] = Computer(self, self.selectColorMenu.getP2Color(), 2, self.board.xTiles - 4,
                                       self.board.yTiles - 4, Player.DIRECT_LEFT)
        # EVE - 2 bots
        elif matchType == 2:
            self.players[1] = Computer(self, self.selectColorMenu.getP1Color(), 1, 3, 3, Player.DIRECT_RIGHT)
            self.players[2] = Computer(self, self.selectColorMenu.getP2Color(), 2, self.board.xTiles - 4,
                                       self.board.yTiles - 4, Player.DIRECT_LEFT)

        # Build match and set program state
        self.match = Match(self, matchType)
        self.state = 'PLAYING_MATCH'


if __name__ == "__main__":
    # Build and start program cycle
    game = Game(120, 60, 10)  # These values can be edited to adjust the board size and square size
    game.eventLoop()
