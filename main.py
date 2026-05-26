from time import sleep
import random

# funkcje

def clear():
    for i in range(40):
        print()

def koniecGry(wyniki, przyczyna, trudnosc):
    print(f"Raport wyprawy '{nazwa_wyprawy}'")
    print(f'Eksplorował {bohater.nazwa}')
    print()
    for klucz, wartosc in wyniki.items():
        print(klucz, ":", wartosc)
    print()
    print(f'Przyczyna: {przyczyna}')
    print('Wybrana trudność: ', 'Łatwy' if trudnosc == 1.25 else 'Średni' if trudnosc == 1.0 else 'Ciężki')
    print(f'Pozastała energia: {max(0, bohater.energia)}')
    print(f'Pozastałe punkty życia: {max(0, bohater.zycie)}')

def wypiszStatus(biom, biomy, bohater):
    print(f'W tej chwili znajdujesz się na biomie: {biom}')
    print(f'Temperatura wynosi: {biomy[biom]}')
    print(f'Minimalna bezpieczna temperatura: {bohater.strength*0.6}')
    print(f'Życie: {bohater.zycie}')
    print(f'Energia: {bohater.energia}')
    print(f'Pozycja: {bohater.koordynaty}')

# klasy

class Player():
    def __init__(self, nazwa, energia, trudnosc):
        self.nazwa = str(nazwa)
        self.energia = int(energia)
        self.zycie = 100
        self.strength = 20 * trudnosc
        self.koordynaty = [0, 0]

    def takeDamage(self, damage):
        self.zycie = self.zycie - damage

    def dealDamage(self, target, amount):
        target.zycie -= amount

# wczytanie danych początkowych

print('Witam w symulatorze wyprawy po lesie!')
print('Dostępne będą zasoby energia i życie, jeśli któryś z nich sie wyczerpie, wtedy gra się zakończy.')
print('Na każdym nowym polu znajduje sie przedmiot. Przedmiot może być dobry i zły.')
print('Dobry przedmiot daje energię i zdrowię jednak zły robi na odwrót.')
print('Celem wyprawy jest przetrwać jak najdłużej. Gdy nie poruszysz się energia będzie spadała wolniej')
print('Powodzenia, i miłego grania!')
sleep(2)
input('Kliknij Enter aby kontynuować...')
clear()
nazwa_wyprawy = input('Jak chcesz nazwać swoją wyprawę w głąb lasu? - ')
nazwa_bohatera = input('Jak nazywa się twoja postać? - ')
wymiary_raw = input('Jakich wymiarów ma być świat? (np. 50x50) - ')
energia_poczatek = input('Z jakim poziomem energii chcesz startować? (domyślnie i maks. 50) - ')
trudnosc = input('Z jakim poziomem trudności chcesz rozpocząć wyprawę? (1 - łatwa, 2 - średnia, 3 - trudna) - ')
input('Kliknij Enter aby rozpocząć przygodę...')
clear()

# sprawdzanie, czy wprowadzone dane są poprawne

if nazwa_wyprawy == '':
    nazwa_wyprawy = 'Nowa Wyprawa'

if nazwa_bohatera == '':
    nazwa_bohatera = 'Bohater'
try:
    a, b = wymiary_raw.split('x')
    a = int(a)
    b = int(b)
except Exception:
    a, b = 50, 50
max_x = (a // 2) - 1
max_y = (b // 2) - 1

if a == '' or b == '':
    a, b = 50, 50

try:
    energia_poczatek = int(energia_poczatek)
except Exception:
    energia_poczatek = 50

try:
    trudnosc = int(trudnosc)
except Exception:
    trudnosc = 2

if trudnosc == 1:
    trudnosc = 1.25
elif trudnosc == 2:
    trudnosc = 1.0
elif trudnosc == 3:
    trudnosc = 0.75
else:
    trudnosc = 1.0

# oznajmienie zmiennych początkowych

graTrwa = True
bohater = Player(nazwa_bohatera, energia_poczatek, trudnosc)
wyniki = {'Całkowity Dystans': 0, 'Odwiedzone Pola': 0, 'Punkty': 0}
biomy = {'Tajga': -2, 'Las liściasty': 8, 'Las Mieszany': 6, 'Las deszczowy': 26, 'Las bagienny': 20, 'Las sosnowy': 6, 'Las górski': 6, 'Spalony las': 18}
listaBiomow = ['Tajga', 'Las liściasty', 'Las Mieszany', 'Las deszczowy', 'Las bagienny', 'Las sosnowy', 'Las górski', 'Spalony las']
biom = random.choice(listaBiomow)
odwiedzonePola = {}
dobrePrzedmioty = ['Kanapka', 'Woda', 'Apteczka', 'Jabłko']
zlePrzedmioty = ['Trujące jagody', 'Kolce', 'Spleśniała kanapka', 'Brudna woda']

# główna pętla gry

while graTrwa:
    wyniki['Punkty'] += 1
    clear()

    # usuwanie wykroczeń

    bohater.zycie = min(100, bohater.zycie)
    bohater.energia = min(50, bohater.energia)

    # resetowanie zmiennych

    zmianaEnergii = 0
    zmianaZycia = 0
    mnoznik = 2 - trudnosc
    ruszac = False
    klucz = tuple(bohater.koordynaty)
    nowePole = False

    # generowanie brakujących pól, jeśli jest taka potrzeba

    if klucz not in odwiedzonePola:
        odwiedzonePola[klucz] = random.choice(listaBiomow)
        nowePole = True
        wyniki['Odwiedzone Pola'] += 1

    biom = odwiedzonePola[klucz]

    # sprawdzenie, czy warunki zakończenia gry zostały osiągnięte

    if bohater.zycie <= 0:
        graTrwa = False
        koniecGry(wyniki, 'Brak punktów życia.', trudnosc)
        break
    elif bohater.energia <= 0:
        graTrwa = False
        koniecGry(wyniki, 'Brak punktów energii.', trudnosc)
        break
    elif bohater.koordynaty[0] > max_x or bohater.koordynaty[0] < -max_x or bohater.koordynaty[1] > max_y or bohater.koordynaty[1] < -max_y:
        graTrwa = False
        koniecGry(wyniki, 'Wyjście poza granice świata.', trudnosc)
        break

    # sprawdzenie, czy bohater jast na polu z niską temperaturą

    if bohater.strength * 0.6 >= biomy[biom]:
        print()
        print('! Uwaga, temperatura jest bardzo niska, co powoduje zwiększenie zużycia energii. !')
        print()
        mnoznik += (abs(biomy[biom] - bohater.strength * 0.6)) / 10

    # wypisanie statusu postaci

    wypiszStatus(biom, biomy, bohater)

    # losowe przedmioty
    if nowePole:
        if random.randint(1,2) == 1:
            znaleziony = random.choice(dobrePrzedmioty)
            zmianaEnergii += random.randint(0, 10)
            zmianaZycia += random.randint(0, 15)
        else:
            znaleziony = random.choice(zlePrzedmioty)
            zmianaEnergii -= random.randint(0, 10)
            zmianaZycia -= random.randint(0, 15)

        print(f'Podczas swojej eksploracji twój bohater natknął się na: {znaleziony}.')
        print(f'{round(zmianaEnergii)} energii')
        print(f'{round(zmianaZycia)} życia')
        print()

    # kolejne akcje

    while True:
        decyzja = input('Chcesz się poruszyć, czy nic nie robić? (P - poruszyć, C - czekać) - ')
        if decyzja.lower() == 'p':
            wyniki['Całkowity Dystans'] += 1
            ruszac = True
            zmianaEnergii -= 5
            break
        if decyzja.lower() == 'c':
            break
        print('Wprowadzono nieprawidłowe dane.')
        print()
        print()

    while ruszac:
        kierunek = input('W jakim kierunku chcesz się poruszyć? (W - góra, A - lewo, S - dół, D - prawo) - ')

        if kierunek.lower() == 'a':
            bohater.koordynaty[1] += 1
            break
        elif kierunek.lower() == 'w':
            bohater.koordynaty[0] += 1
            break
        elif kierunek.lower() == 'd':
            bohater.koordynaty[1] -= 1
            break
        elif kierunek.lower() == 's':
            bohater.koordynaty[0] -= 1
            break
        else:
            print()
            print('Wprowadzono nieprawidłowy kierunek.')
            print()

    bohater.energia += round(zmianaEnergii * mnoznik) - 3
    bohater.zycie += round(mnoznik * zmianaZycia + 1)