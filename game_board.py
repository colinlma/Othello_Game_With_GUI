import tkinter
import game_logic
import user_input_check

'''this implements the game playing and is the module to be run'''

    


class Board(): 
    def __init__(self):

        variables = user_input_check.get_variables()
        board_columns = variables[0]
        columns = board_columns
        
        board_rows = variables[1]
        rows = board_rows
        start = variables[3]
        first_turn = variables[4]
        
        self.game = game_logic.Othello(board_rows, board_columns, first_turn)
        self.board = self.game.new_game_board(start)
        
        self.root_window = tkinter.Tk()
        self.columns = columns
        self.rows = rows
        self.spot_list = []

        self.width = self.columns*100
        self.height = self.rows*100

        self.original_width = self.width + 4
        self.original_height = self.height + 4

        self.frac_radius_x = 50 / self.width
        self.frac_radius_y =  50 / self.height

        self.width_interval = self.width / self.columns
        self.height_interval = self.height / self.rows

        self.square_length_ratio_w = 100 / (self.width + 4)
        self.square_length_ratio_h = 100 / (self.height + 4)
        
        self.canvas=tkinter.Canvas(
        master=self.root_window, width = self.width, height = self.height,
        background = '#10A877')
        self.canvas.grid(
            row = 1, column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.canvas.bind('<Configure>', self.canvas_resized)
        self.canvas.bind('<Button-1>', self.canvas_clicked)
        self.root_window.rowconfigure(0, weight = 1)
        self.root_window.rowconfigure(1, weight = 9)
        self.root_window.columnconfigure(0, weight = 1)

        self.display_score()
        self.make_board(board_columns, board_rows, self.board)
    def display_score(self)-> None:
        '''displays score to user'''
        pass
        if self.game.turn =='B':
            turn = 'Black'
        else:
            turn = 'White'
        self.score_label = tkinter.Label(
            master = self.root_window, width = 10, height = 5,
            text = "Black: {}       White: {} \n{}  ".format(
                self.game.black_count, self.game.white_count, turn))
        self.score_label.grid(
            row = 0, column = 0,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

    def turn_skipped(self) -> None:
        '''tells user when turn is skipped'''
        self.turn_skipped_window = tkinter.Toplevel()
        self.turn_skipped_window.resizable(width = 0, height = 0)
        skipped_label = tkinter.Label(
            master = self.turn_skipped_window,
            text = "No available moves so turn skipped!")
        skipped_label.grid(
            row = 0 , column = 0, padx = 10, pady = 10)
        ok_button = tkinter.Button(
            master = self.turn_skipped_window, text = "OK", command = self.on_skipped_ok)
        ok_button.grid(
            row = 1, column = 0, padx = 10, pady = 10)

        
    def game_over(self) -> None:
        '''tells user the winner'''
        self.game_over_window = tkinter.Toplevel()
        self.game_over_window.resizable(width = 0, height = 0)
        game_over_label = tkinter.Label(
            master = self.game_over_window, text = "Game is over!")
        game_over_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)
        winner = self.game.return_winner(self.how_to_win)
        if winner=='B':
            winner = 'Black'
        elif winner=='W':
            winner = 'White'
        else:
            winner = 'Tie'
        window_label = tkinter.Label(
            master = self.game_over_window, text = "The winner is: {}! \n".format(winner))
        window_label.grid(
            row = 1, column = 0, padx = 10, pady = 10)
        ok_button = tkinter.Button(
            master = self.game_over_window, text = "OK", command = self.on_game_over_ok)
        ok_button.grid(
            row = 2, column = 0, padx = 10, pady = 10)

    def on_game_over_ok(self) -> None:
        '''destroys window on ok'''
        self.game_over_window.destroy()

    def on_skipped_ok(self) -> None:
        '''destroys window on okay'''
        self.turn_skipped_window.destroy()
 
    def make_circle_coordinates(self, column: int, row: int, piece: str) -> None:
        '''makes coordinates for circles proportional to window so window resizing'''
        center_x = (
           self.width_interval * column+1 - self.width_interval * (column-1) + 1) / 2 + (100 / self.original_width * self.width) * column

        center_y = (
            (self.height_interval * row) - (self.height_interval * (row-1))) / 2 + (100 / self.original_height * self.height) * row

        center_x_ratio = (center_x / self.width + center_x) / 2
        center_y_ratio = (center_y / self.height + center_x) / 2
        
        absolute_radius_x = self.frac_radius_x * self.width
        absolute_radius_y = self.frac_radius_y * self.height
               
        self.store_spots(center_x, center_y, absolute_radius_x - 3, absolute_radius_y - 3 , piece)
        
    def store_spots(self, center_x: int, center_y: int, absolute_radius_x: int, absolute_radius_y: int, piece: str) -> None:
        '''stores spots'''
        width1_ratio = (center_x + absolute_radius_x) / self.width 
        height1_ratio = (center_y + absolute_radius_y - 1) / self.height
        width2_ratio = (center_x - absolute_radius_x) / self.width
        height2_ratio = (center_y - absolute_radius_y + 2) / self.height
        spot=(width1_ratio, height1_ratio, width2_ratio, height2_ratio, piece)
        
        self.spot_list.append(spot)

    def canvas_resized(self, event: tkinter.Event) -> None:
        '''called whenever canvas is resized'''
        self.width= self.canvas.winfo_width()
        self.height=self.canvas.winfo_height()
        self.draw_spots()
        
    def canvas_clicked(self, event: tkinter.Event) -> None:
        '''called whenever canvas is clicked'''
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        x_coord = event.x
        y_coord = event.y
        click_coordinate = (x_coord, y_coord)
        self.convert_to_column_and_row(click_coordinate)
        self.valid_move(self.clicked_coordinate)
        
    def convert_to_column_and_row(self, click_coordinate: (int, int)) -> None:
        '''converts the click coordinates to columns/rows'''            
        column = int((click_coordinate[0]  / (self.square_length_ratio_w * self.width)))
        row = int((click_coordinate[1]) / (self.square_length_ratio_h * self.height))
        self.clicked_coordinate = (column, row)

        
    def valid_move(self, coordinate: (int, int))-> None:
        '''checks to see if the column/row is valid'''
        columns = coordinate[1]
        rows = coordinate[0]
        self.game.pieces_on_board()
        
        self.valid_move_list = self.game.create_valid_move_list()
        empty_space_list = self.game.return_empty_spaces_list()
        valid_move = self.game.is_valid_move(
            [rows, columns], empty_space_list, self.valid_move_list)

        if len(empty_space_list)==0:
            self.game_over()
        elif len(self.valid_move_list) == 0:
            if len(self.last_turn_valid_move_list)==0:
                self.game_over()
            else:
                self.turn_skipped()
                self.last_turn_valid_move_list = self.game.opposite_turn()
                self.display_score()
        if valid_move == True:
            self.spot_list=[]
            self.make_circle_coordinates(rows, columns, self.game.turn)

            should_flip = 1
            self.board = self.game.check_adjacent_spaces(
               rows, columns, should_flip)
            self.make_board(self.columns, self.rows, self.board)
            self.canvas.delete(tkinter.ALL)
            self.draw_spots()
            
            self.last_turn_valid_move_list = self.game.opposite_turn()
            self.game.pieces_on_board()
            self.display_score()
        
        self.game.pieces_on_board()
    def make_board(self, board_col: int, board_rows: int, board: [['']]) -> None:
        '''stores spots for each piece on the board'''
        for row in range(0, board_col ):
            for col in range(0,board_rows):
                piece=board[row][col]
                if piece=='*':
                    pass
                else:
                    self.make_circle_coordinates(row, col, piece)
   
    def draw_spots(self)-> None:
        ''' draws spots'''
        
        self.canvas.delete(tkinter.ALL)
        self.draw_board()
        for spot in self.spot_list:
            piece = spot[4]
            if piece == 'B':
                self.canvas.create_oval(
                    spot[0] * self.width, spot[1] * self.height - 5  ,
                    spot[2] * self.width + 5, spot[3] * self.height  + 5,
                    outline = 'red', fill = 'black')
            else:
                self.canvas.create_oval(
                    spot[0] * self.width, spot[1] * self.height - 5 ,
                    spot[2] * self.width + 5, spot[3] * self.height +5 ,
                    outline = 'red', fill = 'white')
    def draw_board(self) -> None:
        '''draws the lines on the board'''
        self.width_interval = self.width / self.columns
        self.height_interval = self.height / self.rows
        self.canvas.create_line(3, self.height + 4,
        3, 4, fill = 'black')
        self.canvas.create_line(self.width, 3,
        4, 3)
        for column in range(0, self.columns + 1):

            self.canvas.create_line(
                self.width_interval*column + 1, self.height + 4,
                self.width_interval*column + 1, 4, fill = 'black')
            

            for row in range(0, self.rows + 1):

                self.canvas.create_line(
                    self.width, self.height_interval*row + 1,
                    4, self.height_interval * row + 1, fill = 'red')

    def start(self)->None:
        '''starts up the loop'''
        self.root_window.mainloop()
        
        




if __name__ == '__main__':
    Board().start()

            

