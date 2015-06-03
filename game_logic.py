#Colin ma 71323642
'''This module contains the game logic necessary for Othello'''

class Invalid_Move_Error(Exception):
    '''Raises exception if the input is an invalid move'''
    pass
class Invalid_Column_Or_Row(Exception):
    '''Raises exception if the row/column don't exist'''
    pass
class Move_After_Game_Over(Exception):
    '''Raises exception if player attempts to make a move after the game finishes'''
    pass


class Othello():
    '''class containing all of the game logic'''    
    def __init__(self, rows:int, columns: int, first_turn: str)->None:
        '''initialize variables'''
        self.rows=rows
        self.columns=columns
        self.last_turn_valid_move_list = []
        self.valid_move_list = []
        self.turn = first_turn
        self.temp_loc = 1
        self.black_count = 2
        self.white_count = 2
        if self.turn=='B':
            self.next_turn = 'W'
        else:
            self.next_turn = 'B'
    def return_state(self):
        return (self.columns, self.rows, self.turn)
    def opposite_turn(self)->[[int,int]]:
        '''sets next turn to opposite player and prepares game for next turn'''
        if self.turn=='B':
            self.turn = 'W'
            self.next_turn = 'B'
        else:
            self.turn= 'B'
            self.next_turn = 'W'
        self.last_turn_valid_move_list = self.valid_move_list
        return self.last_turn_valid_move_list

    def return_winner(self, how_to_win: int)->str:
        '''returns the winner'''
        if len(self.valid_move_list)==0:
            if len(self.last_turn_valid_move_list)==0:
                return self.get_winner(how_to_win) 
        if len(self.empty_space_list)==0:
            return self.get_winner(how_to_win)
        else:
            return False
    def get_winner(self, how_to_win)->str:
        '''determines the winner based on the choice the user selected'''
        if how_to_win==1:
            if self.white_count>self.black_count:
                self.winner='W'
                return 'W'
            elif self.black_count>self.white_count:
                self.winner='B'
                return 'B'
            else:
                self.winner='Tie'
                return 'Tie'
        else:
            if self.white_count<self.black_count:
                self.winner='W'
                return 'W'
            elif self.black_count<self.white_count:
                self.winner='B'
                return 'B'
            else:
                self.winner='Tie'
                return 'Tie'  

    def pieces_on_board(self)->None:
        '''Counts white and black pieces on the board and creaetes lists of locations of them'''
        self.empty_space_list=[]
        self.white_count=0
        self.black_count=0
        self.whites_on_board=[]
        self.blacks_on_board=[]
        for col in range(self.columns):
            for row in range(self.rows):
                piece=self.board[col][row]
                if piece=='*':
                    self.empty_space_list.append([col, row])
                else:
                    if piece=='W':
                        self.white_count+=1
                        self.whites_on_board.append([col,row])
                    elif piece=='B':
                        self.black_count+=1
                        self.blacks_on_board.append([col,row])

    def return_empty_spaces_list(self)-> [[int]]:
        '''returns list of empty spaces on board'''
        return self.empty_space_list

    def create_valid_move_list(self)->[[int]]:
        '''creates a list of valid moves for the current player's turn'''
        self.valid_move_list=[]
        if self.turn=='B':
            enemy_pieces=self.whites_on_board
        else:
            enemy_pieces=self.blacks_on_board
        for index in range(len(enemy_pieces)):
            column=enemy_pieces[index][0]
            row=enemy_pieces[index][1]
            for column_of_grid in range(column-1,column+2):
                for row_of_grid in range(row-1, row+2):
                    try:
                        current_loc=self.board[column_of_grid][row_of_grid]
                        self.check_adjacent_spaces(column_of_grid,row_of_grid,0)
                    except:
                        pass
        self.valid_move_list=self.valid_move_list_clean()
        self.valid_move_list=self.in_valid_moves()
        return self.valid_move_list

    def in_valid_moves(self)->[[int]]:
        '''Checks if the user input is a valid move'''
        temp_list=[]
        for move in self.valid_move_list:
            check=0
            for item in self.empty_space_list:
                if move==item:
                    check=1
            if check==1:
                temp_list.append(move)
        return temp_list
    def valid_move_list_clean(self)->[[int]]:
        '''Removes repeats of the valid move list'''
        temp_list=[]
        for move in self.valid_move_list:
            check=0
            for item in temp_list:
                if move==item:
                    check=1
            if check==0:
                    temp_list.append(move)
        return temp_list
                
            
            
            
    def check_adjacent_spaces(self, input_col: int,input_row: int, should_flip: int)->[list]:
        '''checks adjacent spaces for potentially available moves'''
        self.mov_row=input_row
        self.mov_col=input_col
        self.flip_list=[]
        for column in range(self.mov_col-1,self.mov_col+2):
            for row in range(self.mov_row-1,self.mov_row+2):
                if column!=input_col or row!=input_row:
                    try:
                        check_piece=self.board[column][row]         
                        if check_piece==self.next_turn:
                            self.check_path(column, row, should_flip)
                    except:
                        pass
        return self.board
    def set_piece(self, input_column: int, input_row: int, should_flip: int)->[list]:
        '''calls functions to set the valid player move onto the board'''
        self.mov_row=input_row
        self.mov_col=input_column
        self.flip_list=[]
        for column in range(self.mov_col-1,self.mov_col+2):
            for row in range(self.mov_row-1,self.mov_row+2):
                try:
                    check_piece=self.board[column][row]
                    if check_piece==self.next_turn:
                        if column>=0:
                            if row>=0:
                                self.check_path(column, row, should_flip)
                except:
                    pass
        return self.board
    def create_check_path_vars(self, column: int, row: int)->None:
        '''creates variables for check_path'''
        try:
            self.diff_row=self.mov_row-row
            self.diff_col=self.mov_col-column
            self.new_row=self.mov_row-self.diff_row*self.multiplier
            self.new_col=self.mov_col-self.diff_col*self.multiplier
            if self.new_row>=0:
                if self.new_col>=0:
                    self.temp_loc=self.board[self.new_col][self.new_row]
                    self.flip_list.append([self.new_col, self.new_row])
                else:
                    self.new_col+=column
            else:
                self.new_row+=row
        except:
            pass    

    def check_path(self, column:int, row:int, should_flip:int)->None:
        '''checks the path of the potential available moves'''
        self.multiplier=1
        self.flip_list=[]
        while True:
            try:
                self.create_check_path_vars(column, row)
                if self.temp_loc==self.turn:
                    if column>=0:
                        if row>=0:
                            self.valid_move_list.append([self.mov_col, self.mov_row])
                            if should_flip==1:
                                self.board[self.mov_col][self.mov_row]=self.turn
                                self.flip_pieces() 
                    break
                elif self.temp_loc=='*':
                    break
                elif self.new_col>self.columns or self.new_col<0:
                    break
                elif self.new_row>self.rows or self.new_row<0:
                    break
                self.multiplier+=1
            except:
                pass


    def flip_pieces(self)->None:
        '''flips pieces for a valid player move'''
        for index in range(0, len(self.flip_list)):
            col=self.flip_list[index][0]
            row=self.flip_list[index][1]
            self.board[col][row]=self.turn

    def new_game_board(self, start: int) ->[[]]:
        '''creates a new game board depending on user input'''
        self.board=[]
        for row in range(self.columns):
            board_row = []
            for column in range(self.rows):
                board_row.append('*')
            self.board.append(board_row)       
        self.set_default_pieces(start)
        return self.board
    def set_default_pieces(self, start: int)->None:
        '''sets initial 4 pieces of board'''
        if start==1:
            self.board[self.columns//2-1][self.rows//2-1] = 'W' 
            self.board[self.columns//2-1][self.rows//2] = 'B' 
            self.board[self.columns//2][self.rows//2-1] = 'B'
            self.board[self.columns//2][self.rows//2] = 'W'
        else:
            self.board[self.columns//2-1][self.rows//2-1] = 'B' 
            self.board[self.columns//2-1][self.rows//2] = 'W' 
            self.board[self.columns//2][self.rows//2-1] = 'W'
            self.board[self.columns//2][self.rows//2] = 'B'
    def game_over(self)->None:
        '''determines if game is over'''
        if self.winner==None:
            self.game_over=False
        else:
            self.game_over=True
    def print_score(self):
        '''prints current score'''
        print("Black: {}   White: {}"
              .format(self.black_count, self.white_count))
        print()   

     
    def is_valid_parameters(self, input_rows: str, input_columns: str, board_rows: str, board_columns: str)->bool:
        '''ensures  input is in an acceptable range of board rows and board columsn'''
        try:
            input_rows=int(input_rows)
            input_columns=int(input_columns)
            if input_rows>board_rows:
                print("Invalid input because rows input is larger than board rows")
                raise Invalid_Column_Or_Row
            elif input_rows<0:
                print("Invalid input because row input is less than zero")
                raise Invalid_Column_Or_Row
            elif input_columns>board_columns:
                print("Invalid input because columns input is larger than board columns")
                raise Invalid_Column_Or_Row
            elif input_columns<0:
                print("Invalid input because row input is less than zero")
                raise Invalid_Column_Or_Row
            else:
                return True
        except:
            print("Invalid input. Enter parameters again please.")
            return False
        

    def is_valid_move(self, player_move: [int,int], empty_space_list:[[int]], valid_move_list:[[int]])->bool:
        '''Ensures player input is a valid move'''
        try:
            requirements=0
            for empty_space in empty_space_list:
                if player_move == empty_space:
                    requirements=1
                    break
            if requirements==1:
                for valid_move in valid_move_list:
                    if player_move==valid_move:
                        return True
                raise Invalid_Move_Error
            else:
                raise Invalid_Move_Error
        except:
            return False
