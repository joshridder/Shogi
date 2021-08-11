# -*- coding: utf-8 -*-
'''
Defines the Piece class as a parent class for each of the specific piece classes
Josh Ridder jmr59
'''

class Piece:
    def __init__(self, x, y, team='Bottom', promoted=False):
        self._x = x
        self._y = y
        self._team = team
        self._promoted = promoted
        
    def get_team(self):
        ''' Returns the team the piece belongs to. '''
        return self._team
    
    def is_promoted(self):
        ''' Returns the piece's promoted status '''
        return self._promoted
    
    def get_x(self):
        ''' Returns the piece's x coordinate on the board '''
        return self._x
    
    def get_y(self):
        ''' Returns the piece's y coordinate on the board. '''
        return self._y
    
    def get_tags(self):
        ''' Returns a set of tags used to identify drawn piece shapes on the canvas.
        Used for deleting pieces on the canvas when a piece moves or is captured. '''
        return 'x' + str(self.get_x()) + ', y' + str(self.get_y())
    
    def move(self, x, y):
        ''' Moves the piece to a location and returns a value (True, False, or None for must) that determines 
        whether or not the piece is allowed to promote when it reaches its location. Players are allowed the option
        to promote their pieces when moving them in or out of the three furthest rows from them. '''
        promotable = False
        # checks if piece if moving from a promotable position
        if self.get_team() == 'Top':
            if self.get_y() >= 7:
                promotable = True
        else:
            if self.get_y() <= 3:
                promotable = True
                
        self._x = x
        self._y = y
        
        if promotable:
            return True
        # if piece did not start in a promotable position, check if it is promotable in its new location
        elif self.get_team() == 'Top':
            if self.get_y() >= 7:
                return True
        else:
            if self.get_y() <= 3:
                return True
        return False
        
    def promote(self):
        ''' Promotes the piece. '''
        self._promoted = True
            
    def highlight(self, canvas):
        ''' Highlights clicked piece '''
        X = self.get_x()
        Y = self.get_y()
        canvas.create_rectangle((X * (500/9) - 54), (Y * (500/9) - 59), 
                                (X * (500/9) - 1) , (Y * (500/9) + 3) , 
                                outline='#e0d731', tags='highlight', width=5)
    
    def draw(self, canvas, hats):
        ''' Draw the given self.on the board, with an option 
        for a team-distinguishing 'hat' for each self.'''
        X = self.get_x()
        Y = self.get_y()
        if self.get_team() == 'Top':
            canvas.create_polygon((X * (500/9) - 45), 
                                      (Y * (500/9) - 20),
                                      # ^ lower left ^   v upper left v
                                      (X * (500/9) - 45),
                                      (Y * (500/9) - 53),
                                      # upper right v
                                      (X * (500/9) - 7),
                                      (Y * (500/9) - 53),
                                      # lower right v
                                      (X * (500/9) - 7),
                                      (Y * (500/9) - 20),
                                      # cone v
                                      (X * (500/9) - 26),
                                      (Y * (500/9)),
                                      fill='#ddc363',
                                      tags=['piece', self.get_tags()])
            # white hat for Top player
            if hats:
                canvas.create_polygon((X * (500/9) - 11),
                                      (Y * (500/9) - 18),
                                      (X * (500/9) - 26),
                                      (Y * (500/9) - 4),
                                      (X * (500/9) - 40),
                                      (Y * (500/9) - 18),
                                      fill='#ffffff',
                                      tags=['piece', self.get_tags()])
        elif self.get_team() == 'Bottom':
            canvas.create_polygon((X * (500/9) - 46), 
                                      (Y * (500/9) - 2),
                                      # ^ bottom left ^   v upper left v
                                      (X * (500/9) - 46),
                                      (Y * (500/9) - 35),
                                      # cone v
                                      (X * (500/9) - 27),
                                      (Y * (500/9) - 55),
                                      # upper right v
                                      (X * (500/9) - 7),
                                      (Y * (500/9) - 35),
                                      # lower right v
                                      (X * (500/9) - 7),
                                      (Y * (500/9) - 2),
                                      fill='#ddc363',
                                      tags=['piece', self.get_tags()])
            # black hat for Bottom player   
            if hats:
                canvas.create_polygon((X * (500/9) - 41),
                                      (Y * (500/9) - 38),
                                      # ^ left point ^   v top point v
                                      (X * (500/9) - 27),
                                      (Y * (500/9) - 52),
                                      # v bottom  point v
                                      (X * (500/9) - 12),
                                      (Y * (500/9) - 38),
                                      tags=['piece', self.get_tags()])
        else:
            raise ValueError('Bad team when drawing self.object')
        
        # draw the label for the piece
        label = self.get_chars()
        tags = self.get_tags()
        if self.is_promoted():
            color = '#d12a21'
        else:
            color = 'black'
        if self.get_team() == 'Top':
            canvas.create_text((X*(500/9)-25), (Y*(500/9) - 36),
                                   text=label, tags=['piece', tags], fill=color, font=(10))
        else:
            canvas.create_text((X*(500/9)-26), (Y*(500/9) - 20),
                                   text=label,tags=['piece', tags], fill=color, font=(10))
            
    def highlight_moves(self, moves, canvas):
        ''' Receives a list of (legal) piece moves and draws a circle on each space. '''
        for X_Y in moves:
            X = X_Y[0]
            Y = int(X_Y[1])
            canvas.create_oval((X * 500/9 - 45), (Y * 500/9 - 10),
                                (X * 500/9 - 9), (Y * 500/9 - 45),
                                fill='', tags=['highlight', 'space'], outline='#ea4707', width=4)
            
    def legal_moves(self, board_state):
        '''Finds possible moves, removes moves that are invalid (would make piece land on another of its own team)
        and returns remaining moves as a list. '''
        moves = self.get_moves()
        for p in board_state:
        # disallows moving pieces onto pieces of their own team
            if [p.get_x(), p.get_y()] in moves and (p.get_team() == self.get_team()):
                moves.remove([p.get_x(), p.get_y()])
        return moves