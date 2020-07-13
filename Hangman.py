import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800,500
FPS = 60
RADIUS = 20
GAP = 15

WHITE = (255,255,255)
BLACK = (0,0,0)
win = pygame.display.set_mode((WIDTH,HEIGHT))
images = []
letters = []
words = []

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)

def word_import():
    #importing all the words from the given file
    f = open('words.txt', 'r')
    for line in f:
        words.append(line.strip())
    f.close()
    word = random.choice(words)
    word = word.upper()
    return word

def draw(word, guessed):
    win.fill(WHITE)
    #draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    #draw words
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word +=letter + ""
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word,1, BLACK)
    win.blit(text,(400,200))

    #draw buttons

    for letter in letters:
        x,y,ltr, visible = letter
        if visible:
            pygame.draw.circle(win,BLACK,(x,y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text,(x-text.get_width()/2,y-text.get_height()/2))
    #draw hangman
    win.blit(images[hangman_status],(150,100))
    pygame.display.update()

def display_msg(message):
    pygame.time.delay(500)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2-text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)

def intro():    #intro code screen
    pygame.display.set_caption("Hangman Game!")

    #game title
    win.fill(WHITE)
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 30))

    #user interface buttons
    pygame.draw.rect(win, BLACK, ((325,130), (150,100)), 3)
    text = WORD_FONT.render("PLAY!", 1, BLACK)
    win.blit(text, (340, 160))
    pygame.draw.rect(win, BLACK, ((325,280), (150,100)), 3)
    text = WORD_FONT.render("QUIT!", 1, BLACK)
    win.blit(text, (340, 310))
    text = LETTER_FONT.render("By: Muhammad Hamza", 1, BLACK)
    win.blit(text, (WIDTH/2-text.get_width()/2, 450))
    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(FPS)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            if (m_x >= 325 and m_x <= 475 and m_y >= 130 and m_y <=230):    #if user presses play
                guessed = []
                game(guessed)
                break
            if (m_x >= 325 and m_x <= 475 and m_y >= 280 and m_y <=380):    #if user presses quit
                pygame.quit()

def game(guessed): #full game code
    global hangman_status
    hangman_status = 0
    
    word = word_import()
    print(word)
    clock = pygame.time.Clock()
    run = True

    #loading hangman images
    for i in range(7):
        image = pygame.image.load("images\hangman" + str(i)+ ".png")
        images.append(image)

    #button variables
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(65 + i), True])    #65 = A in ASCII code

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr , visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2) 
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw(word, guessed)

        won = True
        for letter in word:
            if letter not in guessed:
                won  = False
                break
        
        if won:
            display_msg("You WON!")
            break

        if hangman_status == 6:
            display_msg("You LOST!")
            break

def main():
    while 1:
        intro()

main()