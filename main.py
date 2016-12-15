import pygame
import time
import random

pygame.init()

#declaring and initializing colors with RGB values
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

#setting the window parameters and caption
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake AF')

clock = pygame.time.Clock()

AppleThickness = 10
block_size = 10
FPS = 30

direction = ""

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 70)

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    gameLoop()

        gameDisplay.fill(white)
        message_to_screen("Paused", black, -100, "large")
        message_to_screen("Press C to continue or Q to quit", black, 25)
        message_to_screen("Press R to restart", black, 50)
        pygame.display.update()
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

#random variables for apple location
def randAppleGen():
    randAppleX = round(random.randrange(0,display_width-AppleThickness)/10.0)*10.0
    randAppleY = round(random.randrange(0,display_height-AppleThickness)/10.0)*10.0
    return randAppleX, randAppleY

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    gameLoop()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake AF", green, -100, "large")
        message_to_screen("Press P to play or Q to quit", black, 50, "medium")
        message_to_screen("Press P in game to pause", black, 100, "medium")
        pygame.display.update()
        clock.tick(15)


def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

#method used to blit a message to user
def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    #screen_text= font.render(msg, True, color)
    #gameDisplay.blit(screen_text, [display_width/4, display_height/2])
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

#method that holds the game loop
def gameLoop():
    global direction
    gameExit = False
    gameOver = False

    #initializing and declaring the variable for the snake head
    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        #game over event handling
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over",red, -50, "large")
            message_to_screen("Press P to play again or Q to quit", black, 50, "medium")
            pygame.display.update()
            direction = ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_p:
                        gameLoop()

        #event handling for controlling the snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = True
                if event.key == pygame.K_LEFT and direction != "right":
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP and direction != "down":
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_p:
                    pause()
        #if statement to end the game when snake goes off-screen
        if lead_x >= display_width+10 or lead_x <= -10 or lead_y >= display_height+10 or lead_y <= -10:
            gameOver = True


        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        #adds additional segment to the snake, snakeList is a list of snake body coordinates
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score((snakeLength-1)*10)

        pygame.display.update()

        if lead_x == randAppleX and  lead_y == randAppleY:
            randAppleX, randAppleY = randAppleGen()
            snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()
