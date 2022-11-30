class Player:
    def __init__(self, name, mark):
        self.mark = mark
        self.name = name

    def __str__(self):
        return f"{self.mark}"
