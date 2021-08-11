# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a gold subclass of the piece class
@author: Josh
'''

from piece import Piece

class Gold(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'Gold'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        return 'Golds can move one space in any\ndirection except back-diagonally.\n'
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        return u'金' #promoted chars
    
    def move(self, x, y):
        ''' Moves Gold pieces and returns False because Gold pieces cannot promote. '''
        self._x = x
        self._y = y
        return False
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        X = self.get_x()
        Y = self.get_y()
        if self.get_team() == 'Top':
            return [[X-1, Y+1], [X, Y+1], [X+1, Y+1], [X-1, Y], [X+1, Y], [X, Y-1]] # top moves
        return [[X-1, Y-1], [X, Y+1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X, Y-1]] # bottom moves