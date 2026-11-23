import os                                       # läser miljövariabler
from dotenv import load_dotenv                  # Läser in .env-filen
from sqlalchemy import create_engine, text      # Ansluter till databasen och skickar SQL

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