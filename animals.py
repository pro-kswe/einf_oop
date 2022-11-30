class Animals:
    def __init__(self, name, gattung, art, gewicht, laenge, geschwindigkeit, schutz):
        self.name = name
        self.gattung = gattung
        self.art = art
        self.gewicht = gewicht
        self.laenge = laenge
        self.geschwindigkeit = geschwindigkeit
        self.schutz = schutz

    def printInfo(self):
        print(self.name)
        print(self.gattung, self.art)
        print("Gewicht: ", self.gewicht, "kg")
        print("Länge: ", self.laenge, "m")
        print("Geschwindigkeit: ", self.geschwindigkeit)
        print("Schutz: ", self.schutz)

    def getTime(self, strecke):
        if strecke > 0:
            zeit = strecke / (self.geschwindigkeit / 3.6)
            zeit = round(zeit, 2)
            return zeit
        else:
            return 0


an1 = Animals("Blauwal", "Balaenoptera", "musculus", 200000, 32.0, 48, True)
an2 = Animals("Grosser Delphin", "Tursiops", "truncatus", 450, 6.5, 60, False)
an3 = Animals("Roter Thunfisch", "Thunnus", "thynnus", 300, 3.2, 70, False)
an4 = Animals("Schwertfisch", "Xiphias", "gladius", 130, 1.5, 97, False)
an5 = Animals("Grüne Meeresschildkröte", "Chelonia", "mydas", 165, 1.1, 0.5, True)

an1.printInfo()
an2.printInfo()
an3.printInfo()
an4.printInfo()
an5.printInfo()

strecke = int(input("Strecke[m]? "))
print("Dauer für", strecke, "m:")
print("********************")
time = an1.getTime(strecke)
print(an1.name, time, "s")
time = an2.getTime(strecke)
print(an2.name, time, "s")
time = an3.getTime(strecke)
print(an3.name, time, "s")
time = an4.getTime(strecke)
print(an4.name, time, "s")
time = an5.getTime(strecke)
print(an5.name, time, "s")
