import tkinter as tk
import tkinter.simpledialog as dialog
from tkinter import messagebox
from lib import *


class View:
    def __init__(self, controller):
        self.controller = controller


class ConsoleView(View):

    def ask_for_player_information(self):
        print("Please enter information for player 1:")
        name_1 = input("Name? ")
        symbol_1 = input("Symbol? ")
        name_2 = input("Name? ")
        symbol_2 = input("Symbol? ")
        while symbol_2 == symbol_1:
            print("Your symbol is not unique, try again.")
            symbol_2 = input("Symbol? ")
        self.controller.start_game(name_1, symbol_1, name_2, symbol_2)

    def ask_for_field_number(self):
        field_number = int(input("Field number? "))
        self.controller.update_board(field_number)

    @staticmethod
    def show_board(board_fields):
        output = f"{board_fields[0]} | {board_fields[1]} | {board_fields[2]}"
        print(output)
        print(len(output) * "-")
        output = f"{board_fields[3]} | {board_fields[4]} | {board_fields[5]}"
        print(output)
        print(len(output) * "-")
        output = f"{board_fields[6]} | {board_fields[7]} | {board_fields[8]}"
        print(output)

    @staticmethod
    def show_instruction(player):
        print(f"{player.name} it is your turn!")

    @staticmethod
    def show_input_error():
        print(f"Not a valid field, try again.")

    @staticmethod
    def show_winner(player):
        print(f"{player.name} wins.")

    @staticmethod
    def show_draw():
        print(f"Draw!")


class GuiView(View):
    def __init__(self, controller):
        super().__init__(controller)
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.game_frame = tk.Frame(master=self.window, width=400, height=400, background="red")
        self.game_frame.grid(row=0, column=0)

        self.label = tk.Label(master=self.window, text="Game not started.")
        self.label.grid(row=1, column=0, sticky=tk.EW, ipady=10)

        self.questionMarkPhoto = tk.PhotoImage(file="question_mark.png")
        self.spiderPhoto = tk.PhotoImage(file="spider.png")
        self.ladyBugPhoto = tk.PhotoImage(file="ladybug.png")

    def ask_for_player_information(self):
        name = dialog.askstring("Player Information", "Name?")
        self.controller.start_game(name)

    def show_board(self):
        for field_index in range(9):
            button = tk.Button(master=self.game_frame, image=self.questionMarkPhoto)
            button.configure(command=lambda x=field_index + 1: self.controller.sendFieldNumber(x))
            button.configure(width=100, height=100)
            button.grid(row=field_index // 3, column=field_index % 3)

    def update_board(self, field_number, mark):
        field_index = field_number - 1
        selected_button = self.game_frame.grid_slaves(row=field_index // 3, column=field_index % 3)[0]
        if mark == PLAYER_1_MARK:
            photo = self.spiderPhoto
        else:
            photo = self.ladyBugPhoto
        selected_button.configure(image=photo)
        selected_button.configure(state=tk.DISABLED)
        self.window.update()
        self.controller.handle_next_instruction()

    def show_turn_instruction(self):
        self.label.configure(text=f"It is your turn!")

    def show_waiting_instruction(self):
        self.label.configure(text=f"Please wait, other player is playing.")

    @staticmethod
    def show_input_error():
        messagebox.showerror("Input Error", "Not a valid move. Try again.")

    def show_winner(self, player):
        msg = f"{player.name} wins."
        self.label.configure(text=msg)
        messagebox.showinfo("Game Finished", msg)

    def show_draw(self):
        msg = "Draw!"
        self.label.configure(text=msg)
        messagebox.showinfo("Game Finished", msg)

    def lock_buttons(self):
        for field_index in range(9):
            button = self.game_frame.grid_slaves(row=field_index // 3, column=field_index % 3)[0]
            button.configure(state=tk.DISABLED)
        self.window.update()

    def start(self):
        self.window.mainloop()
