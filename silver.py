# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a silver subclass of the piece class
@author: Josh
'''

from piece import Piece

class Silver(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID '''
        return 'Silver'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        if not self.is_promoted():
            return 'Silvers can move one space in\nany direction diagonally or\none space forward.' #unpromoted hint
        return 'Silvers move as a Gold piece\nwhen promoted\n.' #promoted hint
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        return u'銀' #promoted chars
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        X = self.get_x()
        Y = self.get_y()
        if not self.is_promoted():
            if self.get_team() == 'Top':
                return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y-1], [X+1, Y-1]] # unpromoted top moves
            return [[X-1, Y-1], [X, Y-1], [X+1, Y-1], [X-1, Y+1], [X+1, Y+1]] # unpromoted bottom moves
        
        if self.get_team() == 'Top':
            return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted top moves (gold)
        return [[X-1, Y-1], [X, Y+1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X, Y-1]] # promoted bottom moves (gold)