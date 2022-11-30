import crew_mitglied

mitglied_1 = crew_mitglied.CrewMitglied("James Kirk", 34, "Captain", 2265)
mitglied_2 = crew_mitglied.CrewMitglied("Spock", 25, "Science Officer", 2254)
mitglied_3 = crew_mitglied.CrewMitglied("Leonard McCoy", 39, "Chief Medical Officer", 2266)

enterprise = crew_mitglied.Enterprise()
enterprise.hinzufuegen(mitglied_1)
enterprise.hinzufuegen(mitglied_2)
enterprise.hinzufuegen(mitglied_3)
for m in enterprise.mitglieder:
    print(m)