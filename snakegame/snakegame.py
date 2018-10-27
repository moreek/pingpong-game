import pygame
import random
import sys, math, time
from pygame.locals import *

"""
"""

pygame.init()

SCREEN_WD = 48
SCREEN_HT = 32
snake_wd = 10
snake_ht = 10
apple_wd = 10
apple_ht = 10

clock = pygame.time.Clock()
FPS = 100

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

snake = [[12, 13], [11, 13]]
apple = [[32, 13]] 
snake_dir = [12, 13]
snake_tail = [11, 13]

gameScore = 0
snakeLife = 3

frameCount = 0
frameSpeed = 4

speedControl = 1

direction = [False, False, False, False]
collision = False

screen = pygame.display.set_mode((SCREEN_WD * 10, SCREEN_HT * 10))
pygame.display.set_caption('snakegame')


def printTextLine(textContents, text_x, text_y):        #print text that is imputted
    fontObj = pygame.font.Font(None, 32)
    textSurfaceObj = fontObj.render(textContents, True, GREEN)
    textRectObj = textSurfaceObj.get_rect();
    textRectObj.center = (text_x, text_y)
    screen.blit(textSurfaceObj, textRectObj)


def printScore(scoreValue):     #print scoreValue that is imputted
    fontObj = pygame.font.Font(None, 20)
    textSurfaceObj = fontObj.render('Score: %d' % scoreValue, True, GREEN)
    textRectObj = textSurfaceObj.get_rect();
    textRectObj.center = (50, 10)
    screen.blit(textSurfaceObj, textRectObj)

    pygame.draw.line(screen, GREEN, (0, 20), (SCREEN_WD * 10, 20))


def printLife(lifeValue):       #print lifeValue that is imputted
    fontObj = pygame.font.Font(None, 20)
    textSurfaceObj = fontObj.render('Life: %d' % lifeValue, True, GREEN)
    textRectObj = textSurfaceObj.get_rect();
    textRectObj.center = (150, 10)
    screen.blit(textSurfaceObj, textRectObj)


def playSound(soundContents, playNums):     #make sound that is inputted
    pygame.mixer.init()
    pygame.mixer.music.load(soundContents)
    pygame.mixer.music.play(playNums)


def find_dir():     #find front of the snake's head
    snake_x_head = snake[0][0]
    snake_y_head = snake[0][1]

    if direction[0] == True:
        snake_dir[0] = snake_x_head - 1
    if direction[1] == True:
        snake_dir[1] = snake_y_head - 1
    if direction[2] == True:
        snake_dir[0] = snake_x_head + 1
    if direction[3] == True:
        snake_dir[1] = snake_y_head + 1


def draw_game():        #draw snake and apple
    snake_len = len(snake)
    for i in range(0, snake_len):
        pygame.draw.rect(screen, GREEN, ((snake[i][0] * 10), (snake[i][1] * 10), snake_wd, snake_ht))
    draw_head()
    pygame.draw.rect(screen, RED, ((apple[0][0] * 10), (apple[0][1] * 10), snake_wd, snake_ht))


def draw_head():        #draw a line on the snake's head so it could be notified
    if direction[0] == True:
        pygame.draw.rect(screen, RED, ((snake[0][0] * 10), (snake[0][1] * 10), 3, snake_ht))
    elif direction[1] == True:
        pygame.draw.rect(screen, RED, ((snake[0][0] * 10), (snake[0][1] * 10), snake_wd, 3))
    elif direction[2] == True:
        pygame.draw.rect(screen, RED, ((snake[0][0] * 10 + 10), (snake[0][1] * 10), 3, snake_ht))
    elif direction[3] == True:
        pygame.draw.rect(screen, RED, ((snake[0][0] * 10), (snake[0][1] * 10 + 10), snake_wd, 3))


def modify_snake():     #move snake to its direction
    checkCollission()   #check any collision
    snake_eat_apple()   #check snake eats apple

    find_dir()          #find the direction of the snake
    new_dir = [snake_dir[0], snake_dir[1]]
    snake.insert(0, new_dir)    
    snake.pop()


def find_tail():        #find snake's tail
    snake_x_tail = snake[-1][0]
    snake_y_tail = snake[-1][1]

    if direction[0] == True:
        snake_tail[0] = snake_x_tail
        snake_tail[1] = snake_x_tail
    if direction[1] == True:
        snake_tail[0] = snake_x_tail
        snake_tail[1] = snake_y_tail
    if direction[2] == True:
        snake_tail[0] = snake_x_tail
        snake_tail[1] = snake_y_tail
    if direction[3] == True:
        snake_tail[0] = snake_x_tail
        snake_tail[1] = snake_y_tail


def checkCollission():      #check collision wall and body
    global collision, snakeLife

    snake_len = len(snake)
    for i in range(1, snake_len):
        if snake[0] == snake[i]:
            game_init()
            snakeLife -= 1
            break

    if snake[0][0] < 0 or snake[0][0] >= SCREEN_WD or snake[0][1] < 2 or snake[0][1] >= SCREEN_HT:
        game_init()
        snakeLife -= 1

    if snakeLife == 0:
        collision = True


def appleValueIntermingle():        #set the location of the apple(random)
    snake_len = len(snake) 
    i = 0

    while True:
        apple[0][0] = random.randrange(1, SCREEN_WD)
        apple[0][1] = random.randrange(3, SCREEN_HT)

        if snake[i] != apple[0]:
            break

        i += 1
        if i > snake_len:
            i = 0
    

def snake_eat_apple():      #check snake eats apple and add score and speed
    global gameScore, speedControl

    if snake[0] == apple[0]:
        playSound('eatApple.wav', 0)
        
        pygame.draw.rect(screen, BLACK, ((apple[0][0] * 10), (apple[0][1] * 10), 10, 10))
        appleValueIntermingle()

        find_tail()
        snake_tail_len = len(snake)
        snake.insert(snake_tail_len, snake_tail)

        gameScore += 100
        speedControl += 1


def dir_init():     #reset all direction to false
    for i in range(0, 4):
        direction[i] = False


def game_init():        #reset part of the data of the game, if life is 0 reset all 
    global collision, snake, apple, snake_dir, snake_tail, FPS, speedControl, gameScore, snakeLife
    
    snake = [[12, 13], [11, 13]]
    snake_dir = [12, 13]
    snake_tail = [11, 13]
    apple = [[32, 13]]
    FPS = 100
    
    if snakeLife == 0:
        collision = False
        snakeLife = 3
        gameScore = 0
        speedControl = 0
        dir_init()


while True:
    if collision == True:       #if collision is True stop game
        playSound('gameEnd.wav', 0)
        screen.fill(BLACK)
        printTextLine('Press R Button To Restart', 240, 160)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.key == K_r:        #restart game if r key is entered
                    game_init()
        pygame.display.flip()

    if collision == False:      #if collision is False start game
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       #set direction by direction key
                if event.key == K_LEFT:
                    if direction[2] == True:
                        continue
                    dir_init()
                    direction[0] = True
                elif event.key == K_UP:
                    if direction[3] == True:
                        continue
                    dir_init()
                    direction[1] = True
                elif event.key == K_RIGHT:
                    if direction[0] == True:
                        continue
                    dir_init()
                    direction[2] = True
                elif event.key == K_DOWN:
                    if direction[1] == True:
                        continue
                    dir_init()
                    direction[3] = True
        if (direction[0] or direction[1] or direction[2] or direction[3]) != True:
            printTextLine('Press > Button To Start', 240, 160)
        if (direction[0] or direction[1] or direction[2] or direction[3]) == True:
            if frameCount % frameSpeed == 0:        #adjust game speed
                modify_snake()      #move snake to its direction
                frameCount = 0
            draw_game()
        if speedControl % 5 == 0:
            FPS += 5
            speedControl += 1
        printScore(gameScore)
        printLife(snakeLife)
        pygame.display.flip()       #update display
        clock.tick(FPS)
        frameCount += 1