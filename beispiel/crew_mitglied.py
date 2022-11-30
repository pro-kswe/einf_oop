class CrewMitglied:
    def __init__(self, name, alter, position, dienstbeginn):
        self.name = name
        self.alter = alter
        self.position = position
        self.dienstbeginn = dienstbeginn

    def __str__(self):
        return f"{self.name}: {self.alter}"

class Enterprise:
    def __init__(self):
        self.mitglieder = []

    def hinzufuegen(self, mitglied):
        self.mitglieder.append(mitglied)