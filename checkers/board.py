import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, WHITE, BLUE, RED
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_kings = 0
        self.blue_kings = 0
        self.red_left = 12
        self.blue_left = 12
        self.creer_grille()


    def creer_cases(self, window):
        window.fill(WHITE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BLUE, (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def creer_grille(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, RED))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def ajouter_pieces_sur_grille(self, win):
        self.creer_cases(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.create_piece(win)

    def change_position_sur_grille(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move_piece(row, col)
        
        if row == ROWS - 1 or row == 0:
            piece.get_king()
            if piece.color == BLUE:
                self.blue_kings += 1
            else:
                self.red_kings += 1
                
        
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
        
    def get_piece(self, row, col):
        return self.board[row][col]

    def eliminer_pieces(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

    def valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLUE and not piece.king:
            moves.update(self._valid_moves_left(row-1, -1, -1, piece.color, left))
            moves.update(self._valid_moves_right(row-1, -1, -1, piece.color, right))

        if piece.color == RED and not piece.king:
            moves.update(self._valid_moves_left(row+1, ROWS, 1, piece.color, left))
            moves.update(self._valid_moves_right(row+1, ROWS, 1, piece.color, right))
        
        if piece.king:
            direction = [-1,1]
            for d in range (len(direction)):
                moves.update(self._valid_moves_left_king(row+direction[d], self._direction(direction[d]), direction[d], piece.color, left))
                moves.update(self._valid_moves_right_king(row+direction[d], self._direction(direction[d]), direction[d], piece.color, right))

        return moves

    def _valid_moves_left(self, start, stop, step, color, left, pions_manges=[]):
        derniere_piece_tuee = []
        moves = {}
        for r in range(start,stop,step):
            
            if left < 0:
                break
            
            case_adjacente = self.board[r][left]
            if self._est_vide(case_adjacente):
                
                if pions_manges and not derniere_piece_tuee:
                    return moves
                
                elif (r,left) in moves.keys():
                    return moves 
                
                else:
                    moves[(r, left)] = derniere_piece_tuee  + pions_manges
                    if derniere_piece_tuee:
                        moves.update(self._valid_moves_left(r+step, self._direction(step), step, color, left-1,pions_manges=derniere_piece_tuee))
                        moves.update(self._valid_moves_right(r+step, self._direction(step), step, color, left+1,pions_manges=derniere_piece_tuee))

                return moves
            else:
                if case_adjacente.color == color or derniere_piece_tuee:
                    return moves
                else:
                    derniere_piece_tuee = [case_adjacente]
                      
            
            left -= 1
        return moves
              
    
    def _valid_moves_right(self, start, stop, step, color, right, pions_manges=[]):
        derniere_piece_tuee = []
        moves = {}
        for r in range(start,stop,step):
            
            if right >= COLS:
                break
            
            case_adjacente = self.board[r][right]
            if self._est_vide(case_adjacente):
                
                if pions_manges and not derniere_piece_tuee:
                    return moves
                
                elif (r,right) in moves.keys():
                    return moves
                
                else:
                    moves[(r, right)] = pions_manges + derniere_piece_tuee
                    if derniere_piece_tuee: 
                        moves.update(self._valid_moves_left(r+step, self._direction(step), step, color, right-1, pions_manges=derniere_piece_tuee))
                        moves.update(self._valid_moves_right(r+step, self._direction(step), step, color, right+1,pions_manges=derniere_piece_tuee))
                return moves
            
            else:
                if case_adjacente.color == color or derniere_piece_tuee:
                    return moves
                else:
                    derniere_piece_tuee = [case_adjacente]
                    
        
            right += 1
        return moves


        
    def _valid_moves_left_king(self, start, stop, step, color, left, piece_mangees=[], diagonal = "left"):
        
        derniere_piece_tuee = []
        moves = {}
        
        for r in range (start, stop, step):
            if left < 0:
                break
            
            case_adjacente = self.board[r][left]
            
            if self._est_vide(case_adjacente):
                
                if piece_mangees and not derniere_piece_tuee and diagonal != "left":
                    return moves
            
                elif (r,left) in moves.keys():
                    return moves
                
                else:
                    moves[(r,left)] = derniere_piece_tuee + piece_mangees
                    if derniere_piece_tuee:
                        moves.update(self._valid_moves_left_king(r+step, self._direction(step), step, color, left-1, piece_mangees=derniere_piece_tuee))
                        moves.update(self._valid_moves_right_king(r+step, self._direction(step), step, color, left+1, piece_mangees=derniere_piece_tuee))
                        
            else:
                if case_adjacente.color == color or derniere_piece_tuee :
                    return moves
                else:
                    derniere_piece_tuee = [case_adjacente]
            left -= 1
        return moves
    
    def _valid_moves_right_king(self, start, stop, step, color, right, piece_mangees=[], diagonal = "right"):
        derniere_piece_tuee = []
        moves = {}
        for r in range (start, stop, step):
            
            if right >= COLS:
                break
            
            case_adjacente = self.board[r][right]
            if self._est_vide(case_adjacente):
                if piece_mangees and not derniere_piece_tuee and diagonal != "right":
                    return moves
                
                elif (r,right) in moves.keys():
                    return moves
                    
                else:
                    moves[(r,right)] = derniere_piece_tuee + piece_mangees
                    if derniere_piece_tuee:
                        moves.update(self._valid_moves_left_king(r+step, self._direction(step), step, color, right-1, piece_mangees=derniere_piece_tuee))
                        moves.update(self._valid_moves_right_king(r+step, self._direction(step), step, color, right+1, piece_mangees=derniere_piece_tuee))
            else:
                if case_adjacente.color == color or derniere_piece_tuee :
                    return moves
                else:
                    derniere_piece_tuee = [case_adjacente]
            right += 1
        return moves

    def winner(self):
        
        if self.red_left <= 0:
            return BLUE
        elif self.blue_left <= 0:
            return RED
        return None
           
    def evaluate_level_one(self):
        return self.red_left - self.blue_left  

    def evaluate_level_three(self):
        return self.red_left - self.blue_left + (0.5 * self.red_kings - 0.5 * self.blue_kings)
    
    def evaluate_level_two(self):
        center_squares = [(3, 4), (4, 3), (3, 5), (5, 3), (4, 5), (5, 4), (4, 4), (5, 5)]
        score = 0
        for row, col in center_squares:
            piece = self.get_piece(row, col)
            if piece != 0 and not piece.is_king() :
                score += 1
            elif piece != 0 and piece.is_king():
                score += 2
        return score
        
    
    def _direction(self, step):
        if step == -1:
            return -1
        else:
            return ROWS 
    def _piece_couleur_differente(self, piece, color):
        return piece.color != color
    
    def _est_vide(self, current):
        return current == 0
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.blue_left -= 1