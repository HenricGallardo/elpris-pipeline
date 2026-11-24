import os                                       # läser miljövariabler
from dotenv import load_dotenv                  # Läser in .env-filen
from sqlalchemy import create_engine, text      # Ansluter till databasen och skickar SQL
from src.transform import transform             # Hämta receptet från src/transform.py

# --- 1. Hämta inställningarna från .env ---
load_dotenv()                                   # Läs .env och gör raderna till miljövariabler
name = os.getenv("POSTGRES_USER")               # Användarnamn
password = os.getenv("POSTGRES_PASSWORD")       # Lösenord
db = os.getenv("POSTGRES_DB")                   # Databasens namn

# --- 2. Skapa anslutningen ---
# Mallen: typ://användare:lösenord@dator:port/databas
engine = create_engine(f"postgresql://{name}:{password}@localhost:5432/{db}")

# --- 3. Testa anslutningen ---
with engine.connect() as conn:                          # Öppna anslutningen (stängs automatiskt efteråt)
    result = conn.execute(text("SELECT version();"))    # Fråga databasen vilken version den är
    print(result.scalar())                              # Skriv ut svaret

# --- 4. Hämta den rena tabellen ---
df = transform()                                        # Kör transform och ta emot den rena tabellen
# print(df.shape)                                         # Hur många rader och kolumner (bör vara 124416+ och 9)

# --- 5. Skriv tabellen till databasen ---
df.to_sql(
    "prices",              # Tabellens namn i databasen
    engine,                # Anslutningen: vilken databas vi skriver till
    if_exists="replace",   # Om tabellen redan finns: ersätt den
    index=False,           # Ta inte med pandas radnummer (0, 1, 2 ...) som en kolumn
)
print("Klart! Allting fungerade som tänkt!")