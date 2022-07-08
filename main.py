# Imports the Pygame moduke as well as the Board file
import pygame, time
from pygame.locals import *
import Board


# Starts the Pygame module
pygame.init()
pygame.mixer.quit()

# Sets the width and height of the Pygame window and then creates it
width = 800
height = 800
screen = pygame.display.set_mode((width, height))

# Imports the background image, scales up (doubles the size) and stores its coordinates
background = pygame.image.load("BackgroundBoard.png")
background = pygame.transform.scale(background, (800, 800))

# Instantiates a Board object from the Board class in the Board file
board = Board.Board()

# Loops through and uses counter to get the card name
# Instatiates a Card object with the card name and colour
for counter in range(1, 14):
    board.addCard(str(counter) + 's')
    board.addCard(str(counter) + 'c')
    board.addCard(str(counter) + 'd')
    board.addCard(str(counter) + 'h')

# Shuffles the cards and then deals the cards out
board.shuffleCards()
board.deal()


# Procedure to update the screen 
def updateBoard():
    # Shows the background image
    screen.blit(background, (0, 0))
    # Calls the displayBoard which loops through each card and displays them
    board.displayBoard(screen)


# Main game loop
while not board.gameWon:
    time.sleep(0.0166)
    # Checks for user inputs
    for event in pygame.event.get():
        # Checks if the user has closed the window, if so end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # If the user has left clicked call the update method
        elif event.type == pygame.MOUSEBUTTONDOWN:
            updateBoard()
            pygame.display.flip()
            board.update()
            board.checkForWin()

    # Calls the update procedure and then updates the Pygame window
    updateBoard()
    pygame.display.flip()

# If the game has been won
print('Game Over - You Win')