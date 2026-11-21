# Anteckningar: elpris-pipeline

## Status
- [x] Extract: hämtar elpriser för SE1–SE4, 2026-01-01 → 2026-11-20 (124 416 rader)
      Sparas i data/raw/prices.json (ignoreras av git)
- [x] Transform: rensade kolumner, svensk tid, hjälpkolumner
      (date, hour, minute, weekday 1–7, month, is_weekend)
- [x] PostgreSQL körs i Docker (docker-compose.yml)
      Användare: postgres, lösenord: elpris, databas: postgres, port: 5432
- [ ] sqlalchemy + psycopg2-binary installerade
- [ ] Load: spara den rena tabellen i PostgreSQL   ← BÖRJA HÄR

## Nästa steg
1. Starta Docker Desktop
2. Kör `docker compose up -d` och kolla med `docker ps`
3. Testa anslutningen i load.py med `SELECT version();`
4. Gör transform.py till en funktion så att load.py kan använda den
5. Skriv tabellen till databasen med df.to_sql()

## Senare
- Export till Excel → Power BI
- Tester (pytest) + CI (GitHub Actions)
- Helgdagar som extra data
- Fullstack-app: FastAPI + React (TypeScript), kvartsdiagram per elområde

## Bra kommandon
- `docker compose up -d`: starta databasen
- `docker compose down`: stoppa den (datan finns kvar)
- `docker compose exec db psql -U postgres`: gå in i databasen (`\q` för att gå ut)