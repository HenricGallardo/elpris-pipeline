from src.extract import extract      # Knappen: hämta data
from src.transform import transform  # Knappen: rensa data
from src.load import load            # Knappen: spara i databasen


def main():
    extract()                        # 1. Hämta från API:t och spara prices.json
    df = transform()                 # 2. Läs filen, rensa och få tillbaka tabellen
    load(df)                         # 3. Skicka tabellen till databasen


if __name__ == "__main__":
    main()