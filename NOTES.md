# Anteckningar: elpris-pipeline

## Status
- [x] Extract: hämtar elpriser för SE1–SE4, från 2026-01-01 till date.today()
      Sparas i data/raw/prices.json (ignoreras av git)
- [x] Transform: rensade kolumner, svensk tid, hjälpkolumner
      (date, hour, minute, weekday 1–7, month, is_weekend)
      transform.py är en funktion, transform(), med test-utskrifter
      i if __name__ == "__main__"
- [x] PostgreSQL körs i Docker (docker-compose.yml)
      Användare: henrik, databas: elpris, port: 5432
      Lösenord och inställningar ligger i .env (ignoreras av git), mall i .env.example
- [x] sqlalchemy, psycopg2-binary och python-dotenv installerade
- [x] load.py ansluter till databasen och hämtar tabellen med transform()
- [ ] Load: skriv tabellen till PostgreSQL med df.to_sql()   ← BÖRJA HÄR

## Nästa steg
1. Starta Docker Desktop och kör `docker compose up -d`
2. Kör `python -m src.load` (inte play-knappen!)
3. Välj tabellnamn och skriv df.to_sql()
4. Kolla tabellen i databasen med SQL

## Senare
- Inkrementell hämtning: hämta bara dagar som saknas i databasen
- main.py som kör extract → transform → load
- Schemaläggning: kör pipelinen automatiskt varje dag
- Export till Excel → Power BI
- Tester (pytest) + CI (GitHub Actions)
- Helgdagar som extra data
- Fullstack-app: FastAPI + React (TypeScript), kvartsdiagram per elområde

## Bra kommandon
- `docker compose up -d`: starta databasen
- `docker compose down`: stoppa den (datan finns kvar)
- `docker compose down -v`: stoppa och RADERA datan (försiktigt!)
- `docker compose exec db psql -U henrik -d elpris`: gå in i databasen (`\q` för att gå ut)
- `python -m src.load`: kör en fil från projektmappen

## Att komma ihåg
- Kör filer med `python -m src.fil`, inte play-knappen (annars hittas inte `src`)
- Förstå bättre senare: varför importer letas efter från startpunkten