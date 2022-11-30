class Board:
    def __init__(self):
        self.winner = None
        self.fields = [Field(1), Field(2), Field(3), Field(4), Field(5), Field(6), Field(7), Field(8), Field(9)]

    def can_place(self, number):
        if 1 <= number <= 9:
            field = self.fields[number - 1]
            return field.is_selectable()

    def place(self, number, player):
        self.fields[number - 1].owner = player

    def has_winner(self):
        return self.winner is not None

    def is_draw(self):
        count = 0
        for field in self.fields:
            if field.is_selectable():
                count += 1
        return count == 0

    def determine_winner_in_rows(self):
        for i in range(3):
            if self.fields[i * 3] == self.fields[i * 3 + 1] == self.fields[i * 3 + 2]:
                self.winner = self.fields[i * 3].owner

    def determine_winner_in_columns(self):
        for i in range(3):
            if self.fields[i] == self.fields[i + 3] == self.fields[i + 6]:
                self.winner = self.fields[i].owner

    def determine_winner_in_diagonals(self):
        if self.fields[0] == self.fields[4] == self.fields[8]:
            self.winner = self.fields[0].owner
        elif self.fields[2] == self.fields[4] == self.fields[6]:
            self.winner = self.fields[2].owner

    def determine_winner(self):
        self.determine_winner_in_rows()
        self.determine_winner_in_columns()
        self.determine_winner_in_diagonals()


class Field:
    def __init__(self, number):
        self.number = number
        self.owner = None

    def is_selectable(self):
        return self.owner is None

    def __eq__(self, other):
        if isinstance(other, Field):
            if self.owner is not None and other.owner is not None:
                return self.owner.mark == other.owner.mark
        return False

    def __str__(self):
        if self.owner is None:
            return str(self.number)
        else:
            return str(self.owner.mark)
