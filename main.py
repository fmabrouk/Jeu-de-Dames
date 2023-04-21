import pygame
import math
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, LOGO, BACKGROUND, PLAY, BLUE, RED
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
play_button_rect = PLAY.get_rect()
play_button_rect.x = math.ceil(WIDTH/2.6)
play_button_rect.y = math.ceil(HEIGHT/2.5)
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:

        clock.tick(FPS)
        if game.turn == RED:
            value, new_board = minimax(game.get_board(), 2, RED, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (play_button_rect.collidepoint(event.pos)):
                    game.is_started = True
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.choisir_piece(row, col)

        WIN.blit(BACKGROUND, (0, 0))

        if game.is_started:
            game.update()
        else:
            WIN.blit(LOGO, (225, 100))
            WIN.blit(PLAY, play_button_rect)
        pygame.display.flip()

    pygame.quit()


main()
