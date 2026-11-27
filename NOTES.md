# Anteckningar: elpris-pipeline

## Status
- [x] Extract: extract(start) hämtar elpriser för SE1–SE4 från start till date.today()
      Sparas i data/raw/prices.json (ignoreras av git), mappen skapas automatiskt
- [x] Transform: transform() rensar kolumner, svensk tid, hjälpkolumner
      (date, hour, minute, weekday 1–7, month, is_weekend)
- [x] Load: load(df) lägger till rader i tabellen prices
      (if_exists="append", method="multi", chunksize=1000)
      get_latest_date() frågar efter senaste datumet (None om tabellen saknas)
- [x] main.py kör hela pipelinen: extract → transform → load
- [x] Inkrementell hämtning: hämtar bara dagar som saknas
      Tom databas → börjar från FIRST_DATE (2026-01-01)
      Redan uppdaterad → "Inget nytt att hämta"
- [x] Supabase-projekt "elpris" (Europa, Data API av, RLS på, session pooler)
      get_engine() läser DB_*-variablerna och bygger adressen med URL.create,
      drivername "postgresql+psycopg2"
- [x] GitHub Actions kör pipelinen varje dag kl. 06:00 UTC
      (.github/workflows/pipeline.yml)
      Hemligheter i GitHub: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
      Kan köras för hand: Actions → Daily pipeline → Run workflow
- [x] Docker-databas finns kvar lokalt (docker-compose.yml, POSTGRES_*-variablerna)
      men används inte längre av pipelinen

## Nästa steg (välj ett spår)
1. Tester med pytest + få test.yml att köra dem vid varje push
2. Power BI: visualisera datan från Supabase
3. Webbapp: FastAPI + React (TypeScript), kvartsdiagram per elområde

## Senare
- Primärnyckel på (start, area) så att dubbletter inte kan uppstå
- Felhantering i extract (t.ex. om API:t inte svarar)
- Låsa versioner i requirements.txt med ==
- Hämta morgondagens priser när de är publicerade (efter ca 13:00)
- Helgdagar som extra data
- Prognosmodell (ML) för priser längre fram

## Bra kommandon
- `python -m src.main`: kör hela pipelinen (mot Supabase)
- `python -m src.load`: visar senaste datumet i databasen (ofarligt test)
- `git status`: kontrollera ändringar (och att .env inte syns!)
- `docker compose up -d` / `docker compose down`: starta/stoppa den lokala databasen
- `docker compose down -v`: stoppa och RADERA lokal data (försiktigt!)
- `docker compose exec db psql -U henrik -d elpris`: gå in i lokala databasen (`\q` för att gå ut)

## Bra SQL (Supabase → SQL Editor)
- `SELECT COUNT(*) FROM prices;`: antal rader
- `SELECT MAX(date) FROM prices;`: senaste dagen
- `SELECT area, ROUND(AVG(price_sek)::numeric, 2) FROM prices GROUP BY area ORDER BY area;`:
  snittpris per elområde
- `DELETE FROM prices WHERE date >= '2026-11-23';`: radera dagar (glöm inte WHERE!)

## Att komma ihåg
- Kör filer med `python -m src.fil`, inte play-knappen (annars hittas inte `src`)
- Skriv aldrig till databasen med load.py direkt. All skrivning går via main.py
  (annars blir det dubbletter, eftersom load använder append)
- "Fungerar lokalt" ≠ "fungerar i CI": olika versioner av bibliotek kan bete sig olika
  (SQLAlchemy valde psycopg 3 på GitHub). Ange drivrutin uttryckligen, eller lås versioner
- Läs en traceback nerifrån och upp: sista raden är felet
- Supabase gratis: pausas efter 7 dagars inaktivitet (den dagliga körningen håller den vaken)
- GitHub stänger av schemalagda workflows efter 60 dagar utan aktivitet i repot
- Lösenordet finns i .env och i lösenordshanteraren, kan återställas i Supabase
- Förstå bättre senare: varför importer letas efter från startpunkten