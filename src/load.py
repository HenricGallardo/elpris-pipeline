import os                                       # Läser miljövariabler
from dotenv import load_dotenv                  # Läser in .env-filen
from sqlalchemy import create_engine, text      # Ansluter till databasen och skickar SQL


def get_engine():
    """Skapar anslutningen till databasen med inställningarna från .env."""
    load_dotenv()                                                                 # Läs .env
    name = os.getenv("POSTGRES_USER")                                             # Användarnamn
    password = os.getenv("POSTGRES_PASSWORD")                                     # Lösenord
    db = os.getenv("POSTGRES_DB")                                                 # Databasens namn
    engine = create_engine(f"postgresql://{name}:{password}@localhost:5432/{db}") # Skapa anslutningen
    return engine                                                                 # Lämna tillbaka den


def load(df):                                   # Tar emot tabellen som parameter
    """Skriver tabellen till databasen."""
    engine = get_engine()                       # Tryck på knappen och ta emot anslutningen

    df.to_sql(
        "prices",              # Tabellens namn i databasen
        engine,                # Anslutningen: vilken databas vi skriver till
        if_exists="replace",   # Om tabellen redan finns: ersätt den
        index=False,           # Ta inte med pandas radnummer som en kolumn
    )

    with engine.connect() as conn:              # Kontrollera hur många rader som kom in
        count = conn.execute(text("SELECT COUNT(*) FROM prices;")).scalar()
    print(f"Klart! {count} rader i tabellen prices.")


def get_latest_date():
    engine = get_engine()                              # Hämta anslutningen

    with engine.connect() as conn:                     # Ring databasen
        latest = conn.execute(text("SELECT MAX(date) FROM prices;")).scalar()  # Fråga efter senaste dagen

    return latest                                      # Lämna tillbaka svaret

if __name__ == "__main__":                      # Bara när load.py körs direkt
#    print(get_latest_date())                    # Testa: vilket är senaste datumet i databasen?
    from src.transform import transform        
    load(transform())                           # Hämta tabellen och skriv den till databasen