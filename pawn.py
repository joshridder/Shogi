# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a pawn subclass of the piece class
@author: Josh
'''

from piece import Piece

class Pawn(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Pawn'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        if not self.is_promoted():
            return 'Pawns can move one space forward.\n\n'
        return 'Pawns move as a Gold\npiece when promoted.\n'
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        if not self.is_promoted():
            return u'歩'
        return u'と'
    
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
                return [[X, Y+1]]
            return [[X, Y-1]]
        
        # promoted pawns move as a gold piece
        if self.get_team() == 'Top':
            return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y], [X+1, Y], [X, Y-1]]
        # v bottom moves top moves ^ (promoted)
        return [[X-1, Y-1], [X, Y+1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X, Y-1]]