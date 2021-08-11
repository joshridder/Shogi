# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a knight subclass of the piece class
@author: Josh
'''

from piece import Piece

class Knight(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Knight'
    
    def get_text(self):
        ''' Returns help text to display in sidebar. '''
        if not self.is_promoted():
            return 'Knights move two spaces forward\nand one to the right or left.\nCan jump over other pieces.' #unpromoted hint
        return 'Knights move as a Gold piece\nwhen promoted\n.' #promoted hint
    
    def get_chars(self):
        ''' Returns characters to display on piece. '''
        return u'桂'
    
    def move(self, x, y):
        ''' Moves the a pawn to the target location and return a value based on whether the pawn can promote:
        True means the pawn can promote, False means it can't promote, and None means it must promote. '''
        self._x = x
        self._y = y
        
        if self.get_team() == 'Top':
            if self.get_y() > 7:
                return None
            elif self.get_y() == 7:
                return True
        else:
            if self.get_y() < 3:
                return None
            elif self.get_y() == 3:
                return True
        return False
    
    def get_moves(self):
        ''' Returns all possible move locations. '''
        X = self.get_x()
        Y = self.get_y()
        if not self.is_promoted():
            if self.get_team() == 'Top':
                return [[X-1, Y+2], [X+1, Y+2]] # unpromoted top moves
            return [[X-1, Y-2], [X+1, Y-2]] # unpromoted bottom moves
        
        if self.get_team() == 'Top':
            return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted top moves
        return [[X-1, Y-1], [X, Y+1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted bottom moves