import pygame

#Management color without RGB
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
DEFAULT1  = (220,   0,  30)
DEFAULT2  = ( 30, 220,   0)


class SelectColorMenu:
    def __init__(self, gameObj):
        self.game = gameObj

        self.font = pygame.font.SysFont(None, 34)

        self.menuList = ['RED', 'GREEN', 'BLUE', 'Back to Menu']
        self.items = []  # text objects, a list of lists: [text, bitmap, (width, height), (posx, posy)]
        self.activeItem = 0
        self.activeColour = (30, 140, 255)
        self.inactiveColour = (255, 255, 255)
        self.SelectColor = 0
        self.p1Color = DEFAULT1
        self.p2Color = DEFAULT2

        # calculate the positions of the text elements (populates self.items)
        for i, item in enumerate(self.menuList):
            if i == self.activeItem:
                colour = self.activeColour
            else:
                colour = self.inactiveColour
            label = self.font.render(item, 1, colour)

            width = label.get_rect().width
            height = label.get_rect().height + 40

            posx = (self.game.scr_x / 2) - (width / 2)

            total_height = len(self.items) * height
            posy = (self.game.scr_y / 2) - (total_height / 2) + (i * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def eventTick(self, event):
        if event.type == pygame.KEYUP:  # change the active menu entry
            prevActive = self.activeItem

            # change the current active item. Use modular arithmatic to loop around the list.
            if event.key == pygame.K_UP:
                self.activeItem = ((self.activeItem - 1) % len(self.items))
            elif event.key == pygame.K_DOWN:
                self.activeItem = ((self.activeItem + 1) % len(self.items))

            # if we changed active entries, redraw the new active entry in blue and redraw the old one in black
            if prevActive != self.activeItem:
                self.items[self.activeItem][1] = self.font.render(self.items[self.activeItem][0], 1, self.activeColour)
                self.items[prevActive][1] = self.font.render(self.items[prevActive][0], 1, self.inactiveColour)
                self.game.screen.fill((0, 0, 0))
                self.draw()

            # select the color or select to return Main menu
            if event.key == pygame.K_RETURN:
                if self.activeItem == 3:
                    self.game.switchToMainMenu()
            elif event.key == pygame.K_1:
                self.p1Color = self.checkColor(self.activeItem)
            elif event.key == pygame.K_2:
                self.p2Color = self.checkColor(self.activeItem)

    def draw(self):
        # Build title text
        # Add announce to select color
        self.game.screen.fill(BLACK)
        titleFont = pygame.font.SysFont(None, 80)
        announceFont = pygame.font.SysFont(None, 50)
        title = titleFont.render("PyTron", 1, WHITE)
        announce_1 = announceFont.render("Press key 1 to change Player 1 Color", 1, WHITE)
        announce_2 = announceFont.render("Press key 2 to change Player 2 Color", 1, WHITE)
        title_width = title.get_rect().width
        announce_1_width = announce_1.get_rect().width
        announce_2_width = announce_2.get_rect().width
        # draw title and announce
        self.game.screen.blit(title, ((self.game.scr_x / 2) - (title_width / 2), 80))
        self.game.screen.blit(announce_1, ((self.game.scr_x / 2) - (announce_1_width / 2), 160))
        self.game.screen.blit(announce_2, ((self.game.scr_x / 2) - (announce_2_width / 2), 200))
        # draw selectable menu options
        for name, label, (width, height), (posx, posy) in self.items:
            self.game.screen.blit(label, (posx, posy))

    #Method to return Color depend on its argument
    def checkColor(self, number):
        if number == 0:
            return RED
        elif number == 1:
            return GREEN
        elif number == 2:
            return BLUE

    #Getter method to return Player 1 color
    def getP1Color(self):
        return self.p1Color

    #Getter method to return Player 2 color
    def getP2Color(self):
        return self.p2Color

