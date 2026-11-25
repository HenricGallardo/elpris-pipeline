from datetime import date, timedelta
from src.extract import extract
from src.transform import transform
from src.load import load, get_latest_date

FIRST_DATE = date(2026, 1, 1)                    # Hur långt bakåt vi hämtar vid första körningen


def main():
    latest = get_latest_date()                   # Fråga databasen: senaste dagen vi har?

    if latest is None:                           # Tom databas: hämta all historik
        start = FIRST_DATE
    else:                                        # Annars: börja dagen efter den senaste
        start = latest + timedelta(days=1)

    if start > date.today():                     # Redan uppdaterad? Då finns inget att göra
        print("Databasen är redan uppdaterad. Inget nytt att hämta.")
        return

    print(f"Hämtar från {start} till {date.today()}")
    extract(start)                               # 1. Hämta bara de dagar som saknas
    df = transform()                             # 2. Rensa dem
    load(df)                                     # 3. Lägg till dem i databasen


if __name__ == "__main__":
    main()