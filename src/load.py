import os                                       # Läser miljövariabler
from dotenv import load_dotenv                  # Läser in .env-filen
from sqlalchemy import create_engine, text, inspect     # Ansluter till databasen och skickar SQL


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
        if_exists="append",    # Lägg till de nya raderna (skapar tabellen om den inte finns)
        index=False,           # Ta inte med pandas radnummer som en kolumn
    )

    with engine.connect() as conn:              # Kontrollera hur många rader som kom in
        count = conn.execute(text("SELECT COUNT(*) FROM prices;")).scalar()
    print(f"Klart! {count} rader i tabellen prices.")


def get_latest_date():
    """Returnerar senaste datumet i tabellen prices, eller None om tabellen saknas."""
    engine = get_engine()

    if not inspect(engine).has_table("prices"):  # Finns tabellen inte än? 
        return None                              # Då finns inget senaste datum

    with engine.connect() as conn:
        latest = conn.execute(text("SELECT MAX(date) FROM prices;")).scalar()

    return latest                                # Ett datum, eller None om tabellen är tom



if __name__ == "__main__":                      # Bara när load.py körs direkt
    print(get_latest_date())                    # Testa: vilket är senaste datumet i databasen?
