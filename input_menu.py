import tkinter
import user_input_check
'''This module creates an input menu to prompt user for information using tkinter'''

class Input_Window():
    def __init__(self):

        self.input_window = tkinter.Tk()
        self.input_window.resizable(
            width = 0, height = 0)

        title_menu = tkinter.Label(
            master = self.input_window,
            text = "Enter valid inputs for each respective label")
        title_menu.grid(
            row = 0, column = 0, columnspan = 1, padx = 10, pady = 10)

        column_label = tkinter.Label(
            master = self.input_window,
            text ="Columns (must be between 4 and 16, and must be even): ")
        column_label.grid(
            row = 1, column = 0, columnspan = 2, padx = 10, sticky = tkinter.W)
        
        self.column_entry = tkinter.Entry(
            master = self.input_window, width = 5)
        self.column_entry.grid(
            row = 1, column = 2, padx = 10, pady = 10, sticky = tkinter.E)
        

        row_label = tkinter.Label(
            master = self.input_window,
            text = "Rows(must be between 4 and 16, and must be even): ")
        row_label.grid(
            row = 2, column = 0, columnspan = 2, padx = 10, sticky = tkinter.W)
        
        self.row_entry = tkinter.Entry(
            master = self.input_window, width = 5)
        self.row_entry.grid(
            row = 2, column = 2, padx = 10, pady = 10, sticky = tkinter.E)

        determine_win_label = tkinter.Label(
            master = self.input_window,
            text = "Do you want to win by who has the most, or least tiles? (Input most or least) ")
        determine_win_label.grid(
            row = 3, column = 0,sticky = tkinter.W)

        self.determine_win_entry = tkinter.Entry(
            master = self.input_window, width = 5)
        self.determine_win_entry.grid(
            row = 3, column = 2, padx = 10, pady = 10, sticky = tkinter.E)

        
        determine_start_label = tkinter.Label(
            master = self.input_window,
            text = "Black or white to start in the upper left corner? ")
        determine_start_label.grid(
            row = 4, column = 0, sticky = tkinter.W)

        self.determine_start_entry=tkinter.Entry(
            master = self.input_window, width = 10)
        self.determine_start_entry.grid(
            row = 4, column = 2, pady = 10, padx = 10, sticky = tkinter.E)
        

        determine_first_turn_label = tkinter.Label(
            master = self.input_window,
            text ="Black or white to have first turn? ")
        determine_first_turn_label.grid(
            row = 5, column = 0, pady = 10, sticky = tkinter.W)

        self.determine_first_turn_entry = tkinter.Entry(
            master = self.input_window, width = 10)
        self.determine_first_turn_entry.grid(
            row = 5, column = 2, padx = 10, pady = 10, sticky = tkinter.E)

        ok_button = tkinter.Button(
            master = self.input_window, font = 15, text = "OK",
            justify = "center", width = 10, height = 5, command = self.on_ok)
        ok_button.grid(
            row = 6, column = 0, padx = 10, pady = 10, sticky = tkinter.S)
        
    def on_ok(self) -> None:
        '''activated on ok'''
        first_turn = self.determine_first_turn_entry.get()
        start_position = self.determine_start_entry.get()
        how_to_win = self.determine_win_entry.get()
        rows =  self.row_entry.get()
        columns = self.column_entry.get()
        self.input = (columns, rows, how_to_win, start_position, first_turn)
        self.input_window.destroy()

    def invalid_input_window(self)-> None:
        '''opens up an error window if one or more inputs was invalid'''
        self.invalid_window = tkinter.Tk()
        self.invalid_window.resizable(
            width = 0, height =  0)
        
        ok_button = tkinter.Button(
            master = self.invalid_window, text ="OK",
            command = self.on_okay_invalid_button)
        ok_button.grid(
            row = 1, column = 0, padx = 10, pady = 10)

        error_label = tkinter.Label(
            master = self.invalid_window,
            text = "One or more inputs was invalid. Please enter valid input for every entry")
        error_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)
    def on_okay_invalid_button(self)-> None:
        '''destroys window on ok'''
        self.invalid_window.destroy()
    
    def start(self)-> None:
        '''runs the window'''
        self.input_window.mainloop()


