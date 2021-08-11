# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2018
Models a king subclass of the piece class
@author: Josh Ridder jmr59
'''

from piece import Piece

class King(Piece):
    
    def get_id(self):
        ''' Returns the piece's ID. '''
        return 'King'
    
    def get_text(self):
        ''' Returns help text to display in sidebar '''
        return 'Kings move one space in any direction.\n\n'
    
    def get_chars(self):
        ''' Returns characters to display on piece '''
        if self.get_team() == 'Top':
            return u'玉'
        return u'王'
    
    def move(self, x, y):
        ''' Moves the King piece. The King can never promote, so the function always returns False. '''
        self._x = x
        self._y = y
        return False
    
    def get_moves(self):
        ''' Returns all possible move locations '''
        X = self.get_x()
        Y = self.get_y()
        return [[X-1, Y-1], [X, Y-1], [X+1, Y-1], [X-1, Y], [X+1, Y], [X-1, Y+1], [X, Y+1], [X+1, Y+1]]

if __name__ == '__main__':
    k = King(5, 9)
    k.legal_moves([])