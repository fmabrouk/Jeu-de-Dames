import pygame


WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS


BLUE = (46,115,154)
WHITE = (255,255,255)
GREY = (128,128,128)
RED = (255,0,0)
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
GREEN = (0,255,0)
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/background.jpg'),(WIDTH, HEIGHT))
PLAY = pygame.transform.scale(pygame.image.load('assets/play.jpg'), (150, 50))
LOGO = pygame.transform.scale(pygame.image.load('assets/checkers.jpg'), (250, 150))

