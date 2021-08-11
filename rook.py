# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a rook subclass of the piece class
@author: Josh
'''

from piece import Piece

class Rook(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Rook'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        if not self.is_promoted():
            return 'Rooks can move any number of\nspaces horizontally or vertically.\n' #unpromoted hint
        return 'Rooks can move any number of\nspaces horizontally or vertically or\none space diagonally when promoted.' #promoted hint
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        return u'飛' #unpromoted chars
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        moves = []
        for x in range(1, 9):
            # adds spaces to the right and left of location
            X1 = self.get_x() + x
            X2 = self.get_x() - x
            Y = self.get_y()
            moves.append([X1, Y])
            moves.append([X2, Y])
            # adds spaces above and below piece
            X = self.get_x()
            Y1 = self.get_y() + x
            Y2 = self.get_y() - x
            moves.append([X, Y1])
            moves.append([X, Y2])
        if self.is_promoted():
            # adds diagonal one-space moves if promoted
            moves.append([self.get_x() - 1, self.get_y() - 1])
            moves.append([self.get_x() - 1, self.get_y() + 1])
            moves.append([self.get_x() + 1, self.get_y() + 1])
            moves.append([self.get_x() + 1, self.get_y() - 1])
        for X_Y in moves:
            # removes invalid (not on board) moves from output
            X = X_Y[0]
            Y = X_Y[1]
            if X < 1 or Y < 1 or X > 9 or Y > 9:
                moves.remove(X_Y)
        return moves # promoted moves
    
    def legal_moves(self, board_state):
        '''Finds possible moves, removes moves that are invalid 
        due to the current board state, highlights remaining (currently valid) moves,
        and returns them as a list. '''
        moves = self.get_moves()
        for p in board_state:
        # disallows moving pieces onto pieces of their own team
            if [p.get_x(), p.get_y()] in moves and (p.get_team() == self.get_team()):
                moves.remove([p.get_x(), p.get_y()])
        for z in range(1, 9):
            for p in board_state:
                lower_bound = self.get_y() + z
                upper_bound = self.get_y() - z
                if p.get_y() == upper_bound and p.get_x() == self.get_x():
                # block pieces from moving further than the farthest left piece in its path
                    for n in range(upper_bound):
                        try:
                            moves.remove([self.get_x(), n])
                        except:
                            pass
                if p.get_y() == lower_bound and p.get_x() == self.get_x():
                # block pieces from moving further than the farthest right piece in its path
                    for n in range(9, lower_bound, - 1):
                        try:
                            moves.remove([self.get_x(), n])
                        except:
                            pass
                left_bound = self.get_x() - z
                right_bound = self.get_x() + z
                if p.get_x() == left_bound and p.get_y() == self.get_y():
                # block pieces from moving further than the farthest left piece in its path
                    for n in range(left_bound):
                        try:
                            moves.remove([n, self.get_y()])
                        except:
                            pass
                elif p.get_x() == right_bound and p.get_y() == self.get_y():
                # block pieces from moving further than the farthest right piece in its path
                    for n in range(9, right_bound, - 1):
                        try:
                            moves.remove([n, self.get_y()])
                        except:
                            pass
        return moves