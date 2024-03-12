import tkinter

def check_text(text):
    try:
        int_text = int(text)
        if len(text) != len(str(int_text)) or text[-1] == "0":
            return False
        else:
            return True
    except ValueError:
        if text == "\b" or text == "":
            return True
        else:
            return False

def check_input(row, col, text, pre_text):
    if play == False:
        return True
    if pre_text != "":
        if start_entry[int(row)][int(col)] != "":
            return False
        else:
            return check_text(text)
    return check_text(text)

def key_press(event, row, col):
    key = event.keysym
    if start_entry[row][col] == "" and key.isdigit() == True:
        if key != "0":
            entry_list[row][col].delete(0, tkinter.END)
    if key == "Left":
        col -= 1 
        if col == -1:
            col = 8
    if key == "Right":
        col += 1
        if col == 9:
            col = 0
    if key == "Up":
        row -= 1
        if row == -1:
            row = 8
    if key == "Down":
        row += 1
        if row == 9:
            row = 0
    entry_list[row][col].focus_set()

def change_puzzle(change):
    global sudoku_no
    if change == 1:
        sudoku_no += 1
    else:
        sudoku_no -= 1
    load_sudoku(sudoku_no)
    check_button.config(state = "normal")

def state_button():
    if sudoku_no == 0:
        previous_button.config(state = "disabled")
    else:
        previous_button.config(state = "normal")
    if sudoku_no == no_of_puzzle - 1:
        next_button.config(state = "disabled")
    else:
        next_button.config(state = "normal")

def show_sudoku():
    global play
    play = False
    for x in range(0, 9):
        for y in range(0, 9):
            entry_list[x][y].delete(0, tkinter.END)
            entry_list[x][y].insert(0, start_entry[x][y])
            if start_entry[x][y] != "":
                entry_list[x][y].config(fg = "black")
            else:
                entry_list[x][y].config(fg = "green")
    state_button()
    play = True

def load_sudoku(sudoku_no):
    global start_entry, current_entry
    start_entry = []
    current_entry = []
    for x in range(sudoku_no * 10, sudoku_no * 10 + 9):
        start_entry.append(list(text[x][:-1]))
    for x in range(0, 9):
        for y in range(0, 9):
            data = start_entry[x][y]
            if data == " ":
                start_entry[x][y] = ""
            else:
                start_entry[x][y] = int(data)
    for x in start_entry:
        y = x.copy()
        current_entry.append(y)
    show_sudoku()

def show_solution():
    for x in range(0, 9):
        for y in range(0, 9):
            entry_list[x][y].delete(0, tkinter.END)
            entry_list[x][y].insert(0, current_entry[x][y])
    check_button.config(state = "disabled")

def is_valid(num, row, col):
    for x in range(0, 9):
        if current_entry[row][x] == num:
            return False
    for x in range(0, 9):
        if current_entry[x][col] == num:
            return False
    square_row = row // 3
    square_column = col // 3
    for x in range(square_row * 3, (square_row + 1) * 3):
        for y in range(square_column * 3, (square_column + 1) * 3):
            if current_entry[x][y] == num:
                return False
    return True

def solve(row, col):
    if row == 8 and col == 9:
        show_solution()
        return True 
    if col == 9:
        row += 1
        col = 0
    if current_entry[row][col] != "":
        return solve(row, col + 1) 
    for num in range (1, 10):
        if is_valid(num, row, col):
            current_entry[row][col] = num
            if solve(row, col + 1):
                return True
        current_entry[row][col] = ""
    return False

def check_solution():
    for x in range(0, 9):
        for y in range(0, 9):
            if start_entry[x][y] == "":
                num = current_entry[x][y]
                if num == "":
                    return False
                else:
                    current_entry[x][y] = ""
                    if is_valid(num, x, y):
                        current_entry[x][y] = num
                    else:
                        return False
    return True

def check():
    for x in range(0, 9):
        for y in range(0, 9):
            current_entry[x][y] = entry_list[x][y].get()
    if check_solution():
        result_text = "Valid Solution"
    else:
        result_text = "Invalid Solution"
    result_window = tkinter.Toplevel()
    result_window.geometry("+250+300")
    result_window.title("Result")
    tkinter.Label(result_window, text = result_text, font = ("Times New Roman", 22)).pack()
    result_window.mainloop()

def clear():
    for i in range(0, 9):
        for j in range(0, 9):
            entry_list[i][j].delete(0, tkinter.END)
    check_button.config(state = "normal")

def my_info():
    info_window = tkinter.Toplevel()
    info_window.geometry("+1000+300")
    info_window.title("Credit")
    tkinter.Label(info_window, text = "SUNNY KUMAR", font = ("Times New Roman", 22)).pack()
    tkinter.Label(info_window, text = "B Tech in CSE", font = ("Times New Roman", 20)).pack()
    tkinter.Label(info_window, text = "Chandigarh University", font = ("Times New Roman", 18)).pack()
    tkinter.Label(info_window, text = "2021-2025", font = ("Times New Roman", 16)).pack()
    info_window.mainloop()

file = open("Sudoku.txt", "r")
text = file.readlines()
no_of_puzzle = 1 + len(text) // 10
file.close()

window = tkinter.Tk()
window.title("Sudoku")
logo = tkinter.PhotoImage(file = "Sudoku.png")
window.iconphoto(False, logo)
window.geometry("+550+160")

sudoku_no = 0
entry_list = []
for i in range(0, 9):
    sub_list = []
    for j in range(0, 9):
        entry = tkinter.Entry(window, width = 2, borderwidth = 2, font = ("Arial", 20))
        if ((i > 2 and i < 6) and (j < 3 or j > 5)) or ((j > 2 and j < 6) and (i < 3 or i > 5)):
                entry.config(bg = "gray")
        register = entry.register(check_input)
        entry.config(validate = "key", validatecommand = (register, i, j, "%P", "%s"))
        entry.bind("<Key>", lambda event, row = i, col = j : key_press(event, row, col))
        entry.grid(row = i + 1, column = j)
        sub_list.append(entry)
    entry_list.append(sub_list)

clear_button = tkinter.Button(window, text = "Clear", font = ("Helvetica", 15), command = clear)
solution_button = tkinter.Button(window, text = "Solution", font = ("Helvetica", 15), command = lambda : solve(0, 0))
check_button = tkinter.Button(window, text = "Check", font = ("Helvetica", 15), command = check)
previous_button = tkinter.Button(window, text = "Previous", font = ("Helvetica", 15), command = lambda : change_puzzle(0))
credit_button = tkinter.Button(window, text = "Credit", font = ("Helvetica", 15), command = my_info)
next_button = tkinter.Button(window, text = "Next", font = ("Helvetica", 15), command = lambda : change_puzzle(1))

clear_button.grid(row = 10, column = 0, columnspan = 3, pady = 5)
solution_button.grid(row = 10, column = 3, columnspan = 3, pady = 5)
check_button.grid(row = 10, column = 6, columnspan = 3, pady = 5)
previous_button.grid(row = 0, column = 0, columnspan = 3, pady = 5)
credit_button.grid(row = 0, column = 3, columnspan = 3, pady = 5)
next_button.grid(row = 0, column = 6, columnspan = 3, pady = 5)

load_sudoku(sudoku_no)
window.mainloop()