import board

root = board.Tk()
try:
    root.iconbitmap('shogi.ico')
except:
    pass
shogi = board.Shogi_Board(root)
shogi.new_game()
root.mainloop()