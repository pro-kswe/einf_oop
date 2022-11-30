from view import GuiView
import lib


class Controller:
    def __init__(self):
        self.view = GuiView(self)
        self.socket = None
        self.mark = None

    def start(self, socket):
        self.socket = socket
        self.view.ask_for_player_information()

    def start_game(self, name):
        self.mark = self.socket.recv(4096).decode()
        print(f"{self.mark} received")
        self.socket.send(name.encode())
        print("Waiting for another player...")
        name = self.socket.recv(4096).decode()
        print(f"{name} joined")
        self.view.show_board()
        self.handle_next_instruction()
        self.view.start()

    def handle_next_instruction(self):
        instruction = self.socket.recv(4096).decode()
        if instruction == "turn":
            self.view.show_turn_instruction()
        else:
            self.view.show_waiting_instruction()
            fieldnumber = int(self.socket.recv(4096).decode())
            if self.mark == lib.PLAYER_1_MARK:
                mark_other_player = lib.PLAYER_2_MARK
            else:
                mark_other_player = lib.PLAYER_1_MARK
            self.view.update_board(fieldnumber, mark_other_player)

    def sendFieldNumber(self, field_number):
        self.view.update_board(field_number, self.mark)
        self.socket.send(str(field_number).encode())
