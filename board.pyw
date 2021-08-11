# -*- coding: utf-8 -*-
'''
Created on Nov 28, 2018
Sets up a game of shogi with piece classes and pre-defined board state.
@author: Josh Ridder jmr59
'''

from tkinter import *
from default_board_state import *
from copy import deepcopy

class Shogi_Board:
    def __init__(self, master):
        self._master = master
        self._master.title('Shogi')
        self._master.bind('<Button-1>', self.click_event)
        self._master.bind('<Button-3>', self.cancel_button)
        self._master.geometry('') # old was '800x500'
        
        self.board_pieces = deepcopy(board_pieces)
        self.REFERENCE_DICT = {'Pawn':'歩\n', 'Silver':'銀\n', 'Gold':'金\n', 'Knight':'桂\n', 'Lance':'香\n', 'Rook':'飛\n', 'Bishop':'角\n'}
        self.user_wants_highlights = True
        self.user_wants_hats = False
        self.user_is_placing = False
        self.game_over = False
        self.user_is_promoting = False
        self.user_is_placing_piece = None
        self.current_piece = None
        
        self.WIDTH = 500
        self.HEIGHT = self.WIDTH
        self.board = Canvas(self._master, width=self.WIDTH, height=self.HEIGHT, background='#8c5e09', highlightthickness=0)
        self.board.bind('h', self.toggle_hats)
        self.board.bind('<Control-n>', self.ask_for_new_game)
        self.board.grid(row=0, column=0, sticky=N)
        self.board.focus_set()
        frame = Frame(self._master)
        frame.grid(row=0, column=1)
        
        self.current_player = StringVar()
        self.current_player.set('Current player:\nBottom')
        self.current_text = StringVar()
        self.current_text.set('Welcome to Shogi!\n\n')
        Label(frame, textvariable=self.current_player).grid(row=0, column=0, pady=85, padx=85)
        Button(frame, text='Place a piece', command=self.place_menu).grid(row=1, column=0, pady=5, padx=85)
        #Button(frame, text=' Toggle hats ', command=self.toggle_hats).grid(row=3, column=0, pady=5, padx=85)
        Button(frame, text='    Options    ', command=self.option_menu).grid(row=3, column=0, pady=5, padx=85)
        Label(frame, textvariable=self.current_text).grid(row=4, column=0, pady=85)
        self.highlight_text_var = StringVar()
        self.highlight_text_var.set('Move highlights: ON')
        self.hat_text_var = StringVar()
        self.hat_text_var.set('      Hats: OFF      ')
        
        line_x1 = self.WIDTH / 9
        line_x2 = self.WIDTH / 9
        line_y1 = 0
        line_y2 = self.HEIGHT
        for x in range(8):
            self.board.create_line(line_x1, line_y1, line_x2, line_y2, fill='#3a3630')
            line_x1 += (self.WIDTH / 9)
            line_x2 += (self.WIDTH / 9)  
        line_x1 = 0
        line_x2 = self.WIDTH
        line_y1 = self.WIDTH / 9
        line_y2 = self.WIDTH / 9
        for x in range(8):
            self.board.create_line(line_x1, line_y1, line_x2, line_y2, fill='#3a3630')
            line_y1 += (self.WIDTH / 9)
            line_y2 += (self.WIDTH / 9)
        
    def new_game(self):
        ''' Sets pieces to the default layout. '''
        self.current_text.set('Board and captured pieces\nhave been reset.\nがんばれ！')
        try:
            try:
                self.option_window.destroy()
            except AttributeError:
                pass
            self.new_game_window.destroy()
        except AttributeError:
            self.current_text.set('Welcome to Shogi!\n\n')
        self.kill_new_game_window()
        self.board.delete('piece')
        self.board.delete('highlight')
        self.current_player.set('Current player:\nBottom')
        self.board_pieces = deepcopy(board_pieces)
        self.top_stolen_pieces = dict.fromkeys(self.REFERENCE_DICT, 0)
        self.bottom_stolen_pieces = dict.fromkeys(self.REFERENCE_DICT, 0)
        for obj in self.board_pieces:
            obj.draw(self.board, self.user_wants_hats)
            
    def ask_for_new_game(self, *event):
        ''' Used to confirm that players would like to start a new game. '''
        try:
            self.new_game_window.destroy()
        except:
            pass
        self.new_game_window = Toplevel(self._master)
        self.new_game_window.geometry('200x132')
        Label(self.new_game_window, text="Are you sure you'd like to\nstart a new game?", padx=27, pady=10).grid(row=0, column=0, columnspan=2, ipadx=4, ipady=10)
        Button(self.new_game_window, text="Yes", command=self.new_game, padx=5, pady=5).grid(row=1, column=0, padx=28, pady=5, ipadx=5)
        Button(self.new_game_window, text="No", command=self.kill_new_game_window, padx=5, pady=5).grid(row=1, column=1, padx=28, pady=5, ipadx=5)
        
    def kill_new_game_window(self):
        try:
            self.new_game_window.destroy()
        except:
            pass
            
    def switch_player(self, *event):
        ''' Switches the active player, changes the current player label, and removes any highlights on the board. '''
        if not self.game_over:
            if self.current_player.get() == 'Current player:\nTop':
                self.current_player.set('Current player:\nBottom')
                self.current_text.set('Bottom player\'s turn.\n\n')
            else:
                self.current_player.set('Current player:\nTop')
                self.current_text.set('Top player\'s turn.\n\n')
            self.board.delete('highlight')
            
    def toggle_hats(self, *event):
        ''' Redraws pieces with/without hats. '''
        self.board.delete('piece')
        if self.user_wants_hats:
            self.user_wants_hats = False
            self.hat_text_var.set('      Hats: OFF      ')
        else:
            self.user_wants_hats = True
            self.hat_text_var.set('      Hats: ON      ')
        for piece in self.board_pieces:
            piece.draw(self.board, self.user_wants_hats)
            
    def toggle_highlight_moves(self):
        if self.user_wants_highlights:
            self.user_wants_highlights = False
            self.highlight_text_var.set('Move highlights: OFF')
            self.board.delete('space')
        else:
            self.user_wants_highlights = True
            self.highlight_text_var.set('Move highlights: ON')
            if self.current_piece is not None:
                self.current_piece.highlight_moves(self.current_piece.legal_moves(self.board_pieces), self.board)

    def option_menu(self):
        if not self.game_over and not self.user_is_promoting and not self.user_is_placing:
            try:
                self.option_window.destroy()
            except:
                pass
            self.option_window = Toplevel(self._master)
            self.option_window.geometry('300x168')
            self.option_window.title('Options')
            Button(self.option_window, textvariable=self.highlight_text_var, command=self.toggle_highlight_moves, pady=5, padx=5).grid(row=1, column=1, pady=10, padx=80)
            Button(self.option_window, textvariable=self.hat_text_var, command=self.toggle_hats, pady=5, padx=5).grid(row=2, column=1, pady=10, padx=80, ipadx=11)
            Button(self.option_window, text="New Game", command=self.ask_for_new_game, pady=5, padx=5).grid(row=3, column=1, pady=10, padx=80, ipadx=26)
         
    def place_menu(self):
        ''' Gives user a GUI to use to place pieces. '''
        if not self.game_over and not self.user_is_promoting and not self.user_is_placing:
            try:
                self.place_window.destroy()
            except:
                pass
            self.board.delete('highlight')
            self.place_window = Toplevel(self._master)
            #self.place_window.transient(self._master)
            self.place_window.title('Place a piece')
            place_label = StringVar()
            if self.current_player.get() == 'Current player:\nTop':
                pieces = self.top_stolen_pieces
                place_label.set('\n\nTop player\'s captured pieces:\n\n')
            else:
                pieces = self.bottom_stolen_pieces
                place_label.set('\n\nBottom player\'s captured pieces:\n\n')
            Label(self.place_window, textvariable=place_label).grid(row=0, column=2, columnspan=3)
            x = 0
            for p in pieces:
                Button(self.place_window, text=self.REFERENCE_DICT[p] + p + ': ' + str(pieces[p]), pady=25, padx=5,
                       command=lambda ID=p: self.place_button(ID)).grid(row=1, column=x)
                x += 1
            Button(self.place_window, text='Cancel', command=self.cancel_button).grid(row=2, column=2, ipadx=35, ipady=5, pady=15, columnspan=3)
            
    def cancel_button(self, *event):
        ''' Triggers upon right-cliking the board or selecting cancel from the place menu.
        Deletes all highlights on the board or cancels any active place commands, and destroys the place menu. '''
        if self.user_is_placing:
            self.user_is_placing = False
            self.current_text.set('Placement cancelled.\n\n')
        else:
            self.current_piece = None
            self.board.delete('highlight')
            self.current_text.set('\n\n')
        try:
            self.place_window.destroy()
        except:
            pass
            
    def place_button(self, ID):
        ''' Command used by the buttons in the place menu. Enables player to place a type of piece
        if they have a non zero number of that piece. '''
        if self.current_player.get() == 'Current player:\nTop':
            pieces = self.top_stolen_pieces
        else:
            pieces = self.bottom_stolen_pieces
        if pieces[ID] > 0:
            self.user_is_placing = True
            if self.current_player.get() == 'Current player:\nTop':
                self.current_text.set('Now placing:  ' + str(ID) + '\nPlace the piece by clicking a valid space\nor cancel with right click or the cancel button.')
            else:
                self.current_text.set('Now placing:  ' + str(ID) + '\nPlace the piece by clicking a valid space\nor cancel with right click or the cancel button.')
            self.user_is_placing_piece = str(ID)
        
    def promotion_window(self):
        ''' GUI that asks users if they want to promote a piece when it moves into or out of the promotion zone. '''
        if not self.current_piece.is_promoted():
            self.user_is_promoting = True
            self.promo_window = Toplevel(self._master)
            #self.promo_window.geometry
            Label(self.promo_window, text='\n\n\nWould you like to promote the ' + self.current_piece.get_id() + ' you just moved?').grid(row=0, column=1)
            Button(self.promo_window, text='Yes', command=self.promoted).grid(row=1, column=0, padx=25, pady=25, ipadx=15, ipady=15)
            Button(self.promo_window, text='No', command=self.kill_promo_window).grid(row=1, column=2, padx=25, pady=25, ipadx=15, ipady=15)    
    
    def kill_promo_window(self):
        ''' Command used by the 'No' button in the promotion window. '''
        self.promo_window.destroy()
        self.user_is_promoting = False
    
    def promoted(self):
        ''' Command used by the 'Yes' button in the promotion window. 
        Also executes automatically if a piece moves onto a space it must promote on. '''
        self.current_piece.promote()
        self.board.delete(self.current_piece.get_tags())
        self.current_piece.draw(self.board, self.user_wants_hats)
        self.user_is_promoting = False
        try:
            self.promo_window.destroy()
        except:
            pass

    def click_event(self, event):
        ''' Processes user clicks based on if the user is currently placing a piece, promoting a piece, or taking their turn. '''
        if self.user_is_promoting:
        # if user is promoting, give them the promotion GUI in case they've closed it
            try:
                self.promo_window.destroy()
            except:
                pass
            finally:
                self.promotion_window()
        elif event.widget == self.board and not self.game_over:
            self.board.delete('highlight')
            # detect which board space the user has clicked on
            bound_right = self.WIDTH / 9
            bound_left = bound_right - (self.WIDTH/9)
            space_pos_x = 1
            for x in range(9):
                if bound_left < event.x < bound_right:
                    self.clicked_space_x = space_pos_x
                    self.clicked_space_x_tag = 'x' + str(self.clicked_space_x)
                    break
                space_pos_x += 1
                bound_right = space_pos_x * (self.WIDTH / 9)
                bound_left = bound_right - (self.WIDTH / 9)
            space_pos_y = 1
            bound_bottom = self.HEIGHT / 9
            bound_top = bound_bottom - (self.HEIGHT/9)
            for x in range(9):
                if bound_top < event.y < bound_bottom:
                    self.clicked_space_y = space_pos_y
                    self.clicked_space_y_tag = 'y' + str(self.clicked_space_y)
                    break
                space_pos_y += 1
                bound_bottom = space_pos_y * (self.HEIGHT / 9)
                bound_top = bound_bottom - (self.HEIGHT / 9)
            if not self.user_is_placing:
                for p in self.board_pieces:
                    if p.get_team() == 'Top' and self.current_player.get() == 'Current player:\nTop':
                        team_matches = True
                    elif p.get_team() == 'Bottom' and self.current_player.get() == 'Current player:\nBottom':
                        team_matches = True
                    else:
                        team_matches = False
                    if p.get_x() == self.clicked_space_x and p.get_y() == self.clicked_space_y and team_matches:
                        self.current_piece = p
                        self.current_text.set(p.get_text())
                        p.highlight(self.board)
                        if self.user_wants_highlights:
                            p.highlight_moves(p.legal_moves(self.board_pieces), self.board)
                        break
                else:
                    if self.current_piece is not None:
                        if [self.clicked_space_x, self.clicked_space_y] not in self.current_piece.legal_moves(self.board_pieces):
                            self.current_piece = None
                        else:
                            self.board.delete(self.current_piece.get_tags())
                            # moves the current piece. the move method also returns a value based on whether a piece can, can't, or must promote.
                            promo_var = self.current_piece.move(self.clicked_space_x, self.clicked_space_y)
                            if promo_var:
                            # if piece can promote, give user the option to promote the piece
                                self.promotion_window()
                            elif promo_var is None:
                            # if piece must promote, promote it
                                self.promoted()
                        if self.current_piece is not None:
                            for p in self.board_pieces:
                                if p.get_x() == self.current_piece.get_x() and p.get_y() == self.current_piece.get_y() and p.get_team != self.current_piece.get_team() and p is not self.current_piece:
                                    self.board.delete(p.get_tags())
                                    self.board_pieces.remove(p)
                                    if self.current_piece.get_team() == 'Top':
                                        try:
                                            self.top_stolen_pieces[p.get_id()] += 1
                                        except KeyError:
                                            self.end_game()
                                    else:
                                        try:
                                            self.bottom_stolen_pieces[p.get_id()] += 1
                                        except KeyError:
                                            self.end_game()
                                    break
                            self.current_piece.draw(self.board, self.user_wants_hats)
                            self.switch_player()
                            if not promo_var:
                                self.current_piece = None      
                        else:
                            self.current_text.set('\n\n')
            else:
                if self.current_player.get() == 'Current player:\nTop':
                    team = 'Top'
                    pieces = self.top_stolen_pieces
                else:
                    team = 'Bottom'
                    pieces = self.bottom_stolen_pieces
                place_is_legal = True
                for p in self.board_pieces:
                    if p.get_x() == self.clicked_space_x and p.get_y() == self.clicked_space_y:
                        place_is_legal = False
                        self.user_is_placing = False
                        self.current_text.set('Cannot place a piece onto\na space that is already occupied.\nPlace cancelled.')
                        self.place_window.destroy()
                        break
                if place_is_legal:
                    if self.user_is_placing_piece == 'Pawn':
                        for p in self.board_pieces:
                            if p.get_id() == 'Pawn' and not p.is_promoted() and p.get_team() == team and p.get_x() == self.clicked_space_x:
                                place_is_legal = False
                                self.current_text.set('Cannot place a pawn in a row where\nyou already have an unpromoted pawn.\nPlace cancelled.')
                                break
                        if team == 'Top':
                            if self.clicked_space_y == 9:
                                place_is_legal = False
                                self.current_text.set('Cannot place a pawn in a row where\nit cannot move forward.\nPlace cancelled.')
                        else:
                            if self.clicked_space_y == 1:
                                place_is_legal = False
                                self.current_text.set('Cannot place a pawn in a row where\nit cannot move forward.\nPlace cancelled.')
                        if place_is_legal:
                            self.board_pieces.append(Pawn(self.clicked_space_x, self.clicked_space_y, team=team))
                            pieces['Pawn'] -= 1
                        else:
                            self.user_is_placing = False
                            self.place_window.destroy()
                    elif self.user_is_placing_piece == 'Silver':
                        self.board_pieces.append(Silver(self.clicked_space_x, self.clicked_space_y, team=team))
                        pieces['Silver'] -= 1
                    elif self.user_is_placing_piece == 'Gold':
                        self.board_pieces.append(Gold(self.clicked_space_x, self.clicked_space_y, team=team))
                        pieces['Gold'] -= 1
                    elif self.user_is_placing_piece == 'Lance':
                        if team == 'Top':
                            if self.clicked_space_y == 9:
                                place_is_legal = False
                        else:
                            if self.clicked_space_y == 1:
                                place_is_legal = False
                        if place_is_legal:
                            self.board_pieces.append(Lance(self.clicked_space_x, self.clicked_space_y, team=team))
                            pieces['Lance'] -= 1
                        else:
                            self.user_is_placing = False
                            self.place_window.destroy()
                            self.current_text.set('Cannot place a lance in a row where\nit cannot move forward.\nPlace cancelled.')
                    elif self.user_is_placing_piece == 'Knight':
                        if team == 'Top':
                            if self.clicked_space_y > 7:
                                place_is_legal = False
                        else:
                            if self.clicked_space_y < 3:
                                place_is_legal = False
                        if place_is_legal:
                            self.board_pieces.append(Knight(self.clicked_space_x, self.clicked_space_y, team=team))
                            pieces['Knight'] -= 1
                        else:
                            self.user_is_placing = False
                            self.place_window.destroy()
                            self.current_text.set('Cannot place a knight in a row where\nit cannot move forward.\nPlace cancelled.')
                    elif self.user_is_placing_piece == 'Rook':
                        self.board_pieces.append(Rook(self.clicked_space_x, self.clicked_space_y, team=team))
                        pieces['Rook'] -= 1
                    elif self.user_is_placing_piece == 'Bishop':
                        self.board_pieces.append(Bishop(self.clicked_space_x, self.clicked_space_y, team=team))
                        pieces['Bishop'] -= 1
                
                if place_is_legal:
                    self.place_window.destroy()
                    self.board_pieces[-1].draw(self.board, self.user_wants_hats)
                    self.user_is_placing = False
                    self.user_is_placing_piece = None
                    self.switch_player()
                    
    def end_game(self):
        ''' Ends the game. This method is called when a player captures their opponents king. '''
        if self.board_pieces[0].get_team() == 'Top':
            label = 'Top player wins!'
        else:
            label = 'Bottom player wins!'
        self.current_text.set(label)
        self.current_player.set('\n')
        end_game_window = Toplevel(self._master)
        end_game_window.transient(self._master)
        Label(end_game_window, text=label).grid(row=0, column=1, pady=50)
        Button(end_game_window, text='View Board', command=end_game_window.destroy).grid(row=1, column=0, ipadx=15, ipady=15, padx=25, pady=25)
        Button(end_game_window, text='Quit', command=self._master.destroy).grid(row=1, column=2, ipadx=25, ipady=15, padx=25, pady=25)
        self.game_over = True
        
if __name__ == '__main__':
    root = Tk()
    try:
        root.iconbitmap('shogi.ico')
    except:
        pass
    shogi = Shogi_Board(root)
    shogi.new_game()
    root.mainloop()