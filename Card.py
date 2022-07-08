# Import Pygame so can blit/show the cards
import pygame


# The Card Class
class Card:
    # The constructor method
    def __init__(self, source):
        # Loads the front card image using the passed string as part of the file path, scales it up and then gets its coordinates
        self.front = pygame.image.load("Cards/" + source + ".png") 
        self.front = pygame.transform.scale(self.front, (100, 140))

        # Does the same for the back image as well
        self.back = pygame.image.load("Cards/Back.png") 
        self.back = pygame.transform.scale(self.back, (100, 140))

        # Gets the rank of the card by splicing the source string
        if len(source) == 3:
            self.rank = int(source[:2])
        else:
            self.rank = int(source[0])

        # Sets the card suit and colour again by splicing the source string
        if source[-1] == 's':
            self.suit = 0
            self.colour = 'black'
        elif source[-1] == 'c':
            self.suit = 1
            self.colour = 'black'
        elif source[-1] == 'h':
            self.suit = 2
            self.colour = 'red'
        elif source[-1] == 'd':
            self.suit = 3
            self.colour = 'red'

        # Initially sets the card to facing down and an array to store the card's coordinates
        self.facingUp = False
        self.coords = [0, 0]


    # Updates the card's coordinates by setting it to the passed coordinates
    def update(self, coordX, coordY):
        self.coords[0] = coordX
        self.coords[1] = coordY


    # Displays the card, either the front image if facing up or back image if facing down
    def show(self, screen):
        screen.blit(self.front, (self.coords[0], self.coords[1])) if self.facingUp else screen.blit(self.back, (self.coords[0], self.coords[1]))


    # Sets the facingUp property to true, for when the player clicks a front card facing down
    def turnOver(self):
        self.facingUp = True
    

    # Sets the facingUp property to False, for when the hand resets
    def turnBack(self):
        self.facingUp = False
    
    
    # Checks if the passed card object is the opposite colour and one rank back from the current card
    def checkNextValidity(self, nextCard):
        return True if nextCard.colour != self.colour and nextCard.rank == self.rank - 1 else False


    # Checks if the passed mouse coordinates are within the card coordinates
    def checkIfClicked(self, mouseX, mouseY, atFront):
        return True if mouseX > self.coords[0] and mouseX < self.coords[0] + 100 and mouseY > self.coords[1] and mouseY < self.coords[1] + (140 if atFront else 30) else False