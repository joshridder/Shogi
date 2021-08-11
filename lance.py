# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a lance subclass of the piece class
@author: Josh
'''

from piece import Piece

class Lance(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Lance'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        if not self.is_promoted():
            return 'Lances can move any number\nof spaces forward, but cannot\njump over other pieces.' #unpromoted hint
        return 'Lances move as a Gold piece\nwhen promoted.\n' #promoted hint
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        return u'香' #unpromoted chars
    
    def move(self, x, y):
        ''' Moves the a pawn to the target location and return a value based on whether the pawn can promote:
        True means the pawn can promote, False means it can't promote, and None means it must promote. '''
        self._x = x
        self._y = y
        
        if self.get_team() == 'Top':
            if self.get_y() == 9:
                return None
            elif self.get_y() > 6:
                return True
        else:
            if self.get_y() == 1:
                return None
            elif self.get_y() < 4:
                return True
        return False
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        X = self.get_x()
        Y = self.get_y()
        if not self.is_promoted():
            if self.get_team() == 'Top':
                return [[X, Y+1], [X, Y+2], [X, Y+3], [X, Y+4], [X, Y+5], [X, Y+6], [X, Y+7], [X, Y+8]] # unpromoted top moves
            return [[X, Y-1], [X, Y-2], [X, Y-3], [X, Y-4], [X, Y-5], [X, Y-6], [X, Y-7], [X, Y-8]] # unpromoted bottom moves
        
        if self.get_team() == 'Top':
            return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted top moves
        return [[X-1, Y-1], [X, Y+1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted bottom moves
    
    def legal_moves(self, board_state):
        '''Finds possible moves, removes moves that are invalid 
        due to the current board state, highlights remaining (currently valid) moves,
        and returns them as a list. '''
        moves = self.get_moves()
        for p in board_state:
        # disallows moving pieces onto pieces of their own team
            if [p.get_x(), p.get_y()] in moves and (p.get_team() == self.get_team()):
                moves.remove([p.get_x(), p.get_y()])
        
        if not self.is_promoted():
        # detects blocked vertical moves for rooks and lances
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
        return moves