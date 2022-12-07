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
        self.window.geometry("400x400")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.game_frame = tk.Frame(master=self.window, height=400, width=400, background="red")
        self.game_frame.columnconfigure(0, weight=1)
        self.game_frame.rowconfigure(0, weight=1)

        self.connect_frame = tk.Frame(master=self.window, height=400, width=400, background="blue")
        self.connect_frame.columnconfigure(0, weight=1)
        self.connect_frame.rowconfigure(0, weight=1)
        self.connect_frame.grid(row=0, column=0)

        self.name_label = tk.Label(master=self.connect_frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(master=self.connect_frame)
        self.name_entry.grid(row=0, column=1)
        self.ip_label = tk.Label(master=self.connect_frame, text="IP-Adresse:")
        self.ip_label.grid(row=1, column=0)
        self.ip_entry = tk.Entry(master=self.connect_frame)
        self.ip_entry.grid(row=1, column=1)
        self.connect_button = tk.Button(master=self.connect_frame, text="Verbinden", command=self.connect)
        self.connect_button.grid(row=2, column=0, columnspan=2)
        self.status_label = tk.Label(master=self.window, text="Game not started.")
        self.status_label.grid(row=1, column=0, sticky=tk.EW, ipady=10)

        self.waiting_frame = tk.Frame(master=self.window, height=400, width=400, background="yellow")
        self.waiting_frame.columnconfigure(0, weight=1)
        self.waiting_frame.rowconfigure(0, weight=1)

        self.questionMarkPhoto = tk.PhotoImage(file="question_mark.png")
        self.spiderPhoto = tk.PhotoImage(file="spider.png")
        self.ladyBugPhoto = tk.PhotoImage(file="ladybug.png")

    def connect(self):
        name = self.name_entry.get()
        ip = self.ip_entry.get()
        if len(ip) == 0:
            ip = "127.0.0.1"
        self.window.title(f"Tic-Tac-Toe: {name}")
        self.controller.connect(name, ip)

    def show_board(self):
        self.waiting_frame.destroy()
        self.status_label.configure(text="Waiting...")
        self.game_frame.grid(row=0, column=0)
        for field_index in range(9):
            button = tk.Button(master=self.game_frame, image=self.questionMarkPhoto)
            button.configure(command=lambda x=field_index + 1: self.controller.send_field_number(x))
            button.configure(width=100, height=100)
            button.grid(row=field_index // 3, column=field_index % 3)
        self.window.update()

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

    def show_turn_instruction(self):
        self.status_label.configure(text=f"It is your turn!")

    def wait_for_other_player(self, other_player_name):
        self.status_label.configure(text=f"{other_player_name} is playing. Please wait.")
        self.window.update()

    def show_winner_text(self, winner_text):
        self.status_label.configure(text=winner_text)
        self.lock_buttons()
        self.window.update()

    def show_draw(self):
        self.status_label.configure(text="Draw!")
        self.lock_buttons()
        self.window.update()

    def show_waiting(self):
        self.connect_frame.destroy()
        self.waiting_frame.grid(row=0, column=0)
        label = tk.Label(master=self.waiting_frame, text="Waiting for other player...")
        label.grid(row=0, column=0)
        self.window.update()

    @staticmethod
    def show_input_error():
        messagebox.showerror("Input Error", "Not a valid move. Try again.")

    def lock_buttons(self):
        for field_index in range(9):
            button = self.game_frame.grid_slaves(row=field_index // 3, column=field_index % 3)[0]
            button.configure(state=tk.DISABLED)
        self.window.update()

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    GuiView(None).start()
