# Import Pygame, Random and the Card file
import pygame, random
import Card


# Board class
class Board:
    # The contructor method
    def __init__(self): 
        # Two empty arrays to store the unshuffled and the shuffled cards before dealing the board
        self.cards = []
        self.deck = []
        
        # Initialise an array of dimentions 7 x 19 (7 - number of columns, 19 -the maximum number of cards that can possibly be in one column)
        self.board = [[None for row in range(19)] for col in range(7)]
        # Stores the coordinates of the first card in each pile 
        self.boardCoords = [(20, 180), (130, 180), (240, 180), (350, 180), (460, 180), (570, 180), (680, 180)]

        # Stores the end pile cards, initial cards are stored to allow for the logic to work without dealing with an empty array 
        self.endPiles = [[Card.Card('0s')], [Card.Card('0c')], [Card.Card('0h')], [Card.Card('0d')]]
        # Stores the end pile coordinates
        self.endCoords = [(350, 20), (460, 20), (570, 20), (680, 20)]
        # Updates the initail cards in the end piles so they are turned over and have their coordinates stored
        for counter in range(4):
            self.endPiles[counter][0].turnOver()
            self.endPiles[counter][0].update(self.endCoords[counter][0], self.endCoords[counter][1])

        # An array for the hand, and one for cards drawn from the hand
        self.hand = []
        self.flippedHand = []
        # Stores the coordinates for the hand cards
        self.handCoords = [(20, 20), (130, 20), (160, 20), (190, 20)]
        # Boolean to store whether the card has come from the hand or not so it can be replaced if not placed elsewhere
        self.fromHand = False

        # Array to store cards that are being moved (have been picked up)
        self.current = []
        # Similar to the fromHand, allows the card to be replaced in an empty column if not placed elsewhere as only kings are allowed there
        self.fromEmpty = False

        # Stores whether the game has been won or not
        self.gameWon = False
    

    # Instantiates a new card and adds it to the cards array
    def addCard(self, source):
        self.cards.append(Card.Card(source))


    # Shuffles the cards by randomly moving one to another array
    def shuffleCards(self):
        while len(self.cards) > 0:
            self.deck.append(self.cards.pop(random.randrange(0, len(self.cards))))
    

    # Deals the cards
    def deal(self):
        # Deals 7 columns with one more card in each column from left to right
        for col in range(7):
            zero = 0
            for row in range(col + 1):
                self.board[col][zero] = self.deck.pop(0)
                zero += 1

        # Turns over the front card in each column
        for counter in range(7):
            self.board[counter][counter].turnOver()
        # Adds the remaining cards to the hand array
        for counter in range(24):
            self.hand.append(self.deck.pop(0))


    # Update procedure - called when the user clicks the left mouse button
    def update(self):
        # Stores the mouse coordunates
        mouseX, mouseY = pygame.mouse.get_pos()

        # If no cards are being moved
        if len(self.current) == 0:
            # Code to pick up a card from hand
            if len(self.flippedHand) > 0:
                # Checks if the last card in the flippedHand array has been clicked
                if self.flippedHand[-1].checkIfClicked(mouseX, mouseY, True):
                    # Adds it to the current array and removes it from the flippedHand array and signals the card is from the hand incase the user wishes to place the card back if not placed elsewhere
                    self.current.append(self.flippedHand.pop(-1))
                    self.fromHand = True

            # Code to draw 0-3 cards from hand
            if mouseX > self.handCoords[0][0] and mouseX < self.handCoords[0][0] + 100 and mouseY > self.handCoords[0][1] and mouseY < self.handCoords[0][1] + 140:
                    # If there is no more cards in the hand but some in the flippedHand array, it moves them back and flips the back over
                    cards = 0
                    if len(self.hand) == 0 and len(self.flippedHand) > 0:
                        for counter in range(len(self.flippedHand)):
                            self.hand.append(self.flippedHand.pop(0))
                            self.hand[-1].turnBack()
                    # Works out how many cards to draw depending on how many cards left in the hand array
                    elif len(self.hand) >= 3:
                        cards = 3
                    elif len(self.hand) == 2:
                        cards = 2
                    elif len(self.hand) == 1:
                        cards = 1
                    # Draws the number of cards decided above by adding them to the flippedHand array and removes them from the hand array
                    for counter in range(cards):
                        self.flippedHand.append(self.hand.pop(0))
            
            # Checks the board array to see if any cards have been clicked
            for col in range(7):
                # Loops through each column and repeats until the index is set to None
                row = 0
                while self.board[col][row] != None:
                    # Checks if the card was clicked - if the card is at the front of the column then it checks the entire card if not then it only checks the 30px down from its coordinates
                    if self.board[col][row].checkIfClicked(mouseX, mouseY, True if self.board[col][row + 1] == None else False):
                        # If the card if facing down and at the front of the column - if so then if flips the card over
                        if not self.board[col][row].facingUp and self.board[col][row + 1] == None:
                            self.board[col][row].turnOver()
                        # Else if its facing up then it loops through the rest of the cards in the column moving them to the current array 
                        elif self.board[col][row].facingUp:
                            mouseRow = row
                            while self.board[col][mouseRow] != None:
                                self.current.append(self.board[col][mouseRow])
                                self.board[col][mouseRow] = None
                                mouseRow += 1
                            # If the card is at the beginning of the column then store that incase the user wishes to place the card(s) back down
                            if row == 0:
                                self.fromEmpty = True
                    row += 1

            # Loops through each end pile to see if it was clicked and if there is a card there that is not the placeholder
            for counter in range(4):
                if self.endPiles[counter][-1].checkIfClicked(mouseX, mouseY, True) and self.endPiles[counter][-1].rank != 0:
                    # If so move it to the current array and remove it from the end pile
                    self.current.append(self.endPiles[counter].pop(-1))
        
        # Else if there is at least one card in the current array
        else:
            # If there is exactly one card then
            if len(self.current) == 1:
                # Loops through each end pile to see if it was clicked, if the card it the right suit and the rank is one more than the card currently in the end pile
                for counter in range(4):
                    if self.endPiles[counter][-1].checkIfClicked(mouseX, mouseY, True) and self.current[0].suit == counter and self.current[0].rank == self.endPiles[counter][-1].rank + 1:
                        # If so then add it to the corresponding end pile and remove it from the current array
                        self.endPiles[counter].append(self.current.pop(0))
                        # Set the fromHand and fromEmpty to false so that the card can't be placed back in the hand or on an empty colummn
                        self.fromHand = False
                        self.fromEmpty = False
                
                # If there are still cards in the current array then
                if len(self.flippedHand) > 0:
                    # Check if the card came from the hand and if the last card in flippedHand was clicked then
                    if self.fromHand and self.flippedHand[-1].checkIfClicked(mouseX, mouseY, True):
                        # Add the card back to the flippedHand array and remove it from the current array 
                        self.flippedHand.append(self.current.pop(0))
                        # Set the fromHand and fromEmpty to false so that the card can't be placed back in the hand or on an empty colummn
                        self.fromHand = False
                        self.fromEmpty = False
                # Else if the card came from the hand and the flipped hand area was clicked then
                elif self.fromHand and mouseX > self.handCoords[1][0] and mouseX < self.handCoords[1][0] + 100 and mouseY > self.handCoords[1][1] and mouseY < self.handCoords[1][1] + 140:
                    # Add the card back to the flippedHand array and remove it from the current array
                    self.flippedHand.append(self.current.pop(0))
                    # Set the fromHand and fromEmpty to false so that the card can't be placed back in the hand or on an empty colummn
                    self.fromHand = False
                    self.fromEmpty = False

            # If there are cards in the current array then
            if len(self.current) > 0:
                # Loop through the last card in each column to see if it was clicked or if its not flipped over
                for col in range(7):
                    row = 0
                    while self.board[col][row] != None:
                        if self.board[col][row + 1] == None and self.board[col][row].checkIfClicked(mouseX, mouseY, True):
                            '''
                            -------------------- ERROR --------------------
                            Error here to do with self.board[col][row] list index out of error when clicking the card above as it transitions from highlighted to not highlighted
                            I think I fixed it but not sure
                            '''
                            validMove = self.board[col][row].checkNextValidity(self.current[0])
                            if validMove or not self.board[col][row].facingUp:
                                for counter in range(len(self.current)):
                                    # Adds the cards in the current array to the board array after the clicked card
                                    self.board[col][row+1+counter] = self.current.pop(0)
                                    # Set the fromHand and fromEmpty to false so that the card can't be placed back in the hand or on an empty colummn
                                    self.fromHand = False
                                    self.fromEmpty = False
                        row += 1  

                # If there is still cards in the current array
                if len(self.current) > 0:
                    # Loops through each column and checks if the first card slot has been clicked
                    for col in range(7):
                        if mouseX > self.boardCoords[col][0] and mouseX < self.boardCoords[col][0] + 100 and mouseY > self.boardCoords[col][1] and mouseY < self.boardCoords[col][1] + 140 and self.board[col][0] == None:
                            # If the card is a king or came from an empty slot then it adds the cards in the current array to the board array from the first slot
                            if self.current[0].rank == 13 or self.fromEmpty:
                                for counter in range(len(self.current)):
                                    self.board[col][counter] = self.current.pop(0)
                                    # Set the fromHand and fromEmpty to false so that the card can't be placed back in the hand or on an empty colummn
                                    self.fromHand = False
                                    self.fromEmpty = False
                

    # Procedure to display the game
    def displayBoard(self, screen):
        # Loops through the end piles and calls the update and show procedure on each card stored
        for suit in range(4):
            if len(self.endPiles[suit]):
                for counter in range(len(self.endPiles[suit])):
                    self.endPiles[suit][counter].update(self.endCoords[suit][0], self.endCoords[suit][1])
                    self.endPiles[suit][counter].show(screen)

        # Calculates how many cards to be shown for the drawn hand
        if len(self.flippedHand) > 0:
            if len(self.flippedHand) > 2:
                cards = 3
            elif len(self.flippedHand) == 2:
                cards = 2
            elif len(self.flippedHand) == 1:
                cards = 1
            cardArea = 1

            # Loops through and calls the update, turnOver and show procedure on each drawn hand card
            for counter in range(-cards, 0):
                self.flippedHand[counter].update(self.handCoords[cardArea][0], self.handCoords[cardArea][1])
                self.flippedHand[counter].turnOver()
                self.flippedHand[counter].show(screen)
                cardArea += 1

        # If there are cards in the hand array then call the update and show procedure on the last card so the user can see there are still cards in the hand
        if len(self.hand) > 0:
            self.hand[-1].update(self.handCoords[0][0], self.handCoords[0][1])
            self.hand[-1].show(screen)

        # Get the mouse coordinates
        mouseX, mouseY = pygame.mouse.get_pos()
        # Loops through and calls the update and show procedures on each card
        for col in range(7):
            row = 0
            extra = 0
            while self.board[col][row] != None:
                self.board[col][row].update(self.boardCoords[col][0], self.boardCoords[col][1] + (row * 30) + extra)
                self.board[col][row].show(screen)
                # If the mouse is over a card make the cards below display slightly lower so the user can see the hovered card
                if mouseX > self.boardCoords[col][0] and mouseX < self.boardCoords[col][0] + 100 and mouseY > self.boardCoords[col][1] + (row * 30) and mouseY < self.boardCoords[col][1] + (row * 30) + 30:
                    extra += 60
                row += 1
        
        # If there is cards in the current hand then call the update and show procedures on each card, displaying them slightly lower down the screen each time
        if len(self.current) > 0:
            for counter in range(len(self.current)):
                self.current[counter].update(mouseX - 35,  mouseY+(30*counter))
                self.current[counter].show(screen)


    # Checks if the user has won, if the last card in each end pile is a king
    def checkForWin(self):
        won = True
        for counter in range(4):
            if self.endPiles[counter][-1].rank != 13:
                won = False
        self.gameWon = won