# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a bishop subclass of the piece class
@author: Josh
'''

from piece import Piece

class Bishop(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Bishop'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        if not self.is_promoted():
            return 'Bishops can move any number\nof spaces diagonally.\n' #unpromoted hint
        return 'Bishops can move any number of\nspaces diagonally or one space\nhorizontally/vertically when promoted.' #promoted hint
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        return u'角'
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        moves = []
        for x in range(1, 9):
            X = self.get_x() + x
            Y = self.get_y() + x
            moves.append([X, Y])
        for x in range(1, 9):
            X = self.get_x() + x
            Y = self.get_y() - x
            moves.append([X, Y])
        for x in range(1, 9):
            X = self.get_x() - x
            Y = self.get_y() + x
            moves.append([X, Y])
        for x in range(1, 9):
            X = self.get_x() - x
            Y = self.get_y() - x
            moves.append([X, Y])
        if self.is_promoted():
            moves.append([self.get_x() - 1, self.get_y()])
            moves.append([self.get_x() + 1, self.get_y()])
            moves.append([self.get_x(), self.get_y() - 1])
            moves.append([self.get_x(), self.get_y() + 1])
        for X_Y in moves:
        # removes invalid (not on board) moves from output
            X = X_Y[0]
            Y = X_Y[1]
            if X < 1 or Y < 1 or X > 9 or Y > 9:
                moves.remove(X_Y)
        return moves

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
            nw_bound = [self.get_x() - z, self.get_y() - z]
            ne_bound = [self.get_x() + z, self.get_y() - z]
            sw_bound = [self.get_x() - z, self.get_y() + z]
            se_bound = [self.get_x() + z, self.get_y() + z]
            for p in board_state:
                if [p.get_x(), p.get_y()] == nw_bound:
                    # block self. from moving further than the northwest left self.in its path
                    for n in range(9, 0, -1):
                        try:
                            moves.remove([p.get_x() - n, p.get_y() - n])
                        except:
                            pass
                elif [p.get_x(), p.get_y()] == ne_bound:
                    # block self. from moving further than the farthest northeast self.in its path
                    for n in range(9, 0, -1):
                        try:
                            moves.remove([p.get_x() + n, p.get_y() - n])
                        except:
                            pass
                elif [p.get_x(), p.get_y()] == sw_bound:
                    # block self. from moving further than the farthest southwest self.in its path
                    for n in range(1, 9):
                        try:
                            moves.remove([p.get_x() - n, p.get_y() + n])
                        except:
                            pass
                elif [p.get_x(), p.get_y()] == se_bound:
                    # block self. from moving further than the farthest left self.in its path
                    for n in range(9, 0, -1):
                        try:
                            moves.remove([p.get_x() + n, p.get_y() + n])
                        except:
                            pass
        return moves