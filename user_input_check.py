
import input_menu

'''This module checks the input of the user to ensure it is valid'''


def get_variables() -> (int, int, int, int, str) :
    '''fetches inputs for the game'''
    while True:
        user_input_window = input_menu.Input_Window()
        user_input_window.start()
        columns = user_input_window.input[0]
        rows = user_input_window.input[1]
        how_to_win = user_input_window.input[2].upper()
        start = user_input_window.input[3].upper()
        first_turn = user_input_window.input[4].upper()
        check_columns = check_columns_or_rows(columns)
        if check_columns ==True:
            columns=int(columns)
            check_rows = check_columns_or_rows(rows)
            if check_rows == True:
                rows = int(rows)
                check_win_option = check_how_to_win(how_to_win)
                if check_win_option != False:
                    how_to_win = check_win_option   
                    check_start = start_position(start)
                    if check_start != False:
                        start = check_start
                        
                        check_first_turn = black_or_white(first_turn)
                        if check_first_turn != False:
                           first_turn = check_first_turn
                           break
        user_input_window.invalid_input_window()
    return(columns, rows, how_to_win, start, first_turn, check_columns)
                   

def black_or_white(color: str) ->bool:
    '''check valid color input'''
    color = color.upper()
    if color == 'WHITE':
        return 'W'
    elif color == 'BLACK':
        return 'B'
    else:
        return False
def start_position(color: str)-> bool:
    '''check start position'''
    color = color.upper()
    if color == 'WHITE':
        return 1
    elif color == 'BLACK':
        return 2
    return False

def check_how_to_win(how_to_win: str) ->int:
    '''check how to win input'''
    if how_to_win == 'MOST':
        return 1
    elif how_to_win =='LEAST':
        return 2
    else:
        return False
        

def check_columns_or_rows(columns_or_rows: int) ->bool:
    '''makes sure input for columns/rows is valid'''
    try:
        number = int(columns_or_rows)
    except:
        return False
        
    if number%2!=0:
        return False
    elif number < 4:
        return False
    elif number > 16:
        return False
    else:
        return True

