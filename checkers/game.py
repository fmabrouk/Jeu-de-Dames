import pygame
from .constants import RED, BLUE, GREEN, SQUARE_SIZE
from .board import Board




class Game:
    def __init__(self, win):
        self.win = win
        self._init()
        
    def update(self):
        self.board.ajouter_pieces_sur_grille(self.win)
        self.afficher_valid_moves(self.valid_moves)
        pygame.display.update()
        
        
    def _init(self):
        self.is_started = False
        self.valid_moves = {}
        self.selected = None
        self.turn = BLUE
        self.board = Board()
        
    def reset(self):
        self._init()
    
    def winner(self):
        return self.board.winner()
    
    def choisir_piece(self, row, col):
        
        if self._is_piece_choisie():
            result = self._is_moved(row, col)
            if not result:
                self.selected = None
                self.choisir_piece( row, col)
                
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.valid_moves(piece)
            return True
        return False
    
    def _is_piece_choisie(self):
        return self.selected
    
    
    def _is_moved(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.change_position_sur_grille(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.eliminer_pieces(skipped)
            self.changer_tour()
        else:
            return False
        return True
    
           
            
    def changer_tour(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE
            
    def afficher_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
            
    def ai_move(self, board):
        self.board = board
        self.changer_tour()
        
    def get_board(self):
        return self.board
    