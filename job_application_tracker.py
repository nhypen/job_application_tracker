import json
import os

PLIK = "aplikacje.json"

DOZWOLONE_STATUSY = ["wysłane", "rozmowa", "odrzucone", "oferta"]


def wczytaj_dane():
    if os.path.exists(PLIK):
        try:
            with open(PLIK, "r", encoding="utf-8") as plik:
                dane = json.load(plik)
                if isinstance(dane, list):
                    return dane
                else:
                    print("Błąd: dane w pliku mają zły format. Tworzę pustą listę.")
                    return []
        except json.JSONDecodeError:
            print("Błąd: plik jest uszkodzony lub pusty. Tworzę pustą listę.")
            return []
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania danych: {e}")
            return []
    return []


def zapisz_dane(aplikacje):
    try:
        with open(PLIK, "w", encoding="utf-8") as plik:
            json.dump(aplikacje, plik, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania danych: {e}")


def pokaz_statusy():
    print("Dostępne statusy:")
    for status in DOZWOLONE_STATUSY:
        print(f"- {status}")


def dodaj_aplikacje(aplikacje):
    print("\n--- Dodawanie nowej aplikacji ---")
    firma = input("Podaj nazwę firmy: ").strip()
    stanowisko = input("Podaj nazwę stanowiska: ").strip()
    data = input("Podaj datę aplikacji (np. 2026-04-15): ").strip()

    pokaz_statusy()
    status = input("Podaj status: ").strip().lower()

    if not firma or not stanowisko or not data or not status:
        print("Błąd: żadne pole nie może być puste.")
        return

    if status not in DOZWOLONE_STATUSY:
        print("Błąd: podano nieprawidłowy status.")
        return

    aplikacja = {
        "firma": firma,
        "stanowisko": stanowisko,
        "data": data,
        "status": status
    }

    aplikacje.append(aplikacja)
    zapisz_dane(aplikacje)
    print("Aplikacja została dodana.")


def pokaz_aplikacje(aplikacje):
    print("\n--- Lista aplikacji ---")

    if not aplikacje:
        print("Brak zapisanych aplikacji.")
        return

    for i, aplikacja in enumerate(aplikacje, start=1):
        print(f"{i}. Firma: {aplikacja['firma']}")
        print(f"   Stanowisko: {aplikacja['stanowisko']}")
        print(f"   Data aplikacji: {aplikacja['data']}")
        print(f"   Status: {aplikacja['status']}")
        print("-" * 40)


def zmien_status(aplikacje):
    print("\n--- Zmiana statusu aplikacji ---")

    if not aplikacje:
        print("Brak aplikacji do edycji.")
        return

    pokaz_aplikacje(aplikacje)

    try:
        numer = int(input("Podaj numer aplikacji do zmiany statusu: "))
        if numer < 1 or numer > len(aplikacje):
            print("Błąd: nieprawidłowy numer aplikacji.")
            return
    except ValueError:
        print("Błąd: wpisz poprawny numer.")
        return

    pokaz_statusy()
    nowy_status = input("Podaj nowy status: ").strip().lower()

    if nowy_status not in DOZWOLONE_STATUSY:
        print("Błąd: nieprawidłowy status.")
        return

    aplikacje[numer - 1]["status"] = nowy_status
    zapisz_dane(aplikacje)
    print("Status został zaktualizowany.")


def szukaj_aplikacji(aplikacje):
    print("\n--- Wyszukiwanie aplikacji ---")

    if not aplikacje:
        print("Brak aplikacji do wyszukania.")
        return

    fraza = input("Podaj nazwę firmy lub jej fragment: ").strip().lower()

    if not fraza:
        print("Błąd: musisz coś wpisać.")
        return

    znalezione = []

    for aplikacja in aplikacje:
        if fraza in aplikacja["firma"].lower():
            znalezione.append(aplikacja)

    if not znalezione:
        print("Nie znaleziono aplikacji dla podanej frazy.")
        return

    print("\nZnalezione aplikacje:")
    for i, aplikacja in enumerate(znalezione, start=1):
        print(f"{i}. Firma: {aplikacja['firma']}")
        print(f"   Stanowisko: {aplikacja['stanowisko']}")
        print(f"   Data aplikacji: {aplikacja['data']}")
        print(f"   Status: {aplikacja['status']}")
        print("-" * 40)


def usun_aplikacje(aplikacje):
    print("\n--- Usuwanie aplikacji ---")

    if not aplikacje:
        print("Brak aplikacji do usunięcia.")
        return

    pokaz_aplikacje(aplikacje)

    try:
        numer = int(input("Podaj numer aplikacji do usunięcia: "))
        if numer < 1 or numer > len(aplikacje):
            print("Błąd: nieprawidłowy numer aplikacji.")
            return
    except ValueError:
        print("Błąd: wpisz poprawny numer.")
        return

    usunieta = aplikacje.pop(numer - 1)
    zapisz_dane(aplikacje)
    print(f"Usunięto aplikację do firmy: {usunieta['firma']}")


def pokaz_statystyki(aplikacje):
    print("\n--- Statystyki ---")

    if not aplikacje:
        print("Brak danych do wyświetlenia.")
        return

    liczba_wszystkich = len(aplikacje)
    statystyki = {
        "wysłane": 0,
        "rozmowa": 0,
        "odrzucone": 0,
        "oferta": 0
    }

    for aplikacja in aplikacje:
        status = aplikacja["status"]
        if status in statystyki:
            statystyki[status] += 1

    print(f"Liczba wszystkich aplikacji: {liczba_wszystkich}")
    for status, liczba in statystyki.items():
        print(f"{status.capitalize()}: {liczba}")


def menu():
    aplikacje = wczytaj_dane()

    while True:
        print("\n===== JOB APPLICATION TRACKER =====")
        print("1. Dodaj aplikację")
        print("2. Pokaż wszystkie aplikacje")
        print("3. Zmień status aplikacji")
        print("4. Wyszukaj aplikację")
        print("5. Usuń aplikację")
        print("6. Pokaż statystyki")
        print("7. Zakończ program")

        wybor = input("Wybierz opcję (1-7): ").strip()

        if wybor == "1":
            dodaj_aplikacje(aplikacje)
        elif wybor == "2":
            pokaz_aplikacje(aplikacje)
        elif wybor == "3":
            zmien_status(aplikacje)
        elif wybor == "4":
            szukaj_aplikacji(aplikacje)
        elif wybor == "5":
            usun_aplikacje(aplikacje)
        elif wybor == "6":
            pokaz_statystyki(aplikacje)
        elif wybor == "7":
            print("Zamykanie programu. Powodzenia w aplikowaniu o pracę!")
            break
        else:
            print("Błąd: wybierz poprawną opcję od 1 do 7.")


menu()