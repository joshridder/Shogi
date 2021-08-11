'''
Created on Dec 7, 2018

@author: Josh Ridder jmr59
'''

from pawn import Pawn
from gold import Gold
from king import King
from rook import Rook
from lance import Lance
from silver import Silver
from knight import Knight
from bishop import Bishop

board_pieces = [King(x=5, y=1, team='Top'), King(x=5, y=9),
                Bishop(x=2, y=8), Bishop(x=8, y=2, team='Top'),
                Rook(x=8, y=8), Rook(x=2, y=2, team='Top')#real set stops here
                ]

for x in range(1, 10):
#make pawns
    board_pieces.append(Pawn(x=x, y=7))
    board_pieces.append(Pawn(x=x, y=3, team='Top'))
for x in range(2):
#make non-pawn pieces that appear more than once per side on the board
    board_pieces.append(Lance(x=(x*8+1), y=1, team='Top'))
    board_pieces.append(Lance(x=(x*8+1), y=9))
    board_pieces.append(Knight(x=(x*6+2), y=1, team='Top'))
    board_pieces.append(Knight(x=(x*6+2), y=9))
    board_pieces.append(Silver(x=(x*4+3), y=1, team='Top'))
    board_pieces.append(Silver(x=(x*4+3), y=9))
    board_pieces.append(Gold(x=(x*2+4), y=1, team='Top'))
    board_pieces.append(Gold(x=(x*2+4), y=9))
    
if __name__ == '__main__':
    for p in board_pieces:
        print(p.get_id(), 'on', p.get_x(), p.get_y())
    val = input()