from copy import deepcopy
from checkers import board
import pygame


RED = (255,0,0)
BLUE = (46,115,154)



def minimax(position, profondeur, max_player, game):
    if profondeur == 0 or position.winner() != None:
        return position.evaluate(), position
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, profondeur-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('+inf')
        best_move = None
        for move in get_all_moves(position, BLUE, game):
            evaluation = minimax(move, profondeur-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move
        
        
def simulate_move(piece, move, board, game, skip):
    board.change_position_sur_grille(piece, move[0], move[1])
    if skip:
        board.remove(skip)
        
    return board
        
def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.valid_moves(piece)
        for move, skip in valid_moves.items():
            
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves


