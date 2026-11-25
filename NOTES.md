# Anteckningar: elpris-pipeline

## Status
- [x] Extract: extract(start) hämtar elpriser för SE1–SE4 från start till date.today()
      Sparas i data/raw/prices.json (ignoreras av git)
- [x] Transform: transform() rensar kolumner, svensk tid, hjälpkolumner
      (date, hour, minute, weekday 1–7, month, is_weekend)
- [x] PostgreSQL körs i Docker (docker-compose.yml)
      Användare: henrik, databas: elpris, port: 5432
      Lösenord och inställningar ligger i .env (ignoreras av git), mall i .env.example
- [x] Load: load(df) lägger till rader i tabellen prices (if_exists="append")
      get_latest_date() frågar efter senaste datumet (None om tabellen saknas)
- [x] main.py kör hela pipelinen: extract → transform → load
- [x] Inkrementell hämtning fungerar (testat genom att radera dagar)
- [x] Supabase-projekt "elpris" skapat (Europa, Data API av, RLS på)
- [x] Supabase-uppgifter i .env: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
      (session pooler, fungerar både lokalt och från GitHub Actions)
- [ ] Koppla pipelinen till Supabase   ← BÖRJA HÄR

## Nästa steg
1. Ändra get_engine() i load.py så att den läser DB_*-variablerna
   (bygg adressen säkert, lösenordet kan innehålla specialtecken)
2. Kör `python -m src.main` mot Supabase (tom databas → hämtar från 2026-01-01)
3. Kolla tabellen i Supabase (Table Editor)
4. GitHub Actions: kör main.py automatiskt varje dag
   (lösenorden som GitHub Secrets)

## Senare
- Export till Excel → Power BI
- Tester (pytest) + CI (GitHub Actions)
- Primärnyckel på (start, area) så att dubbletter inte kan uppstå
- Felhantering i extract (t.ex. om API:t inte svarar)
- Helgdagar som extra data
- Fullstack-app: FastAPI + React (TypeScript), kvartsdiagram per elområde

## Bra kommandon
- `docker compose up -d`: starta databasen
- `docker compose down`: stoppa den (datan finns kvar)
- `docker compose down -v`: stoppa och RADERA datan (försiktigt!)
- `docker compose exec db psql -U henrik -d elpris`: gå in i databasen (`\q` för att gå ut)
- `python -m src.main`: kör hela pipelinen
- `python -m src.load`: visar senaste datumet i databasen (ofarligt test)

## Bra SQL
- `SELECT COUNT(*) FROM prices;`: antal rader
- `SELECT MAX(date) FROM prices;`: senaste dagen
- `SELECT area, AVG(price_sek) FROM prices GROUP BY area;`: snittpris per elområde
- `DELETE FROM prices WHERE date >= '2026-11-23';`: radera dagar (glöm inte WHERE!)

## Att komma ihåg
- Kör filer med `python -m src.fil`, inte play-knappen (annars hittas inte `src`)
- Skriv aldrig till databasen med `python -m src.load`. All skrivning går via main.py
  (annars blir det dubbletter, eftersom load använder append)
- Förstå bättre senare: varför importer letas efter från startpunkten
## Att komma ihåg
- Supabase gratis: pausas efter 7 dagars inaktivitet
- Lösenordet finns i .env och i lösenordshanteraren, kan återställas i Supabase