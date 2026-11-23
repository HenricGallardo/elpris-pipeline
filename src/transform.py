import pandas as pd                                         # Bibliotek för att arbeta med tabeller

# --- 1. Läs in rådatan ---
df = pd.read_json("data/raw/prices.json")                   # Läs in rådatan som en tabell

# --- 2. Rensa kolumner ---
df = df.drop(columns=["EXR", "EUR_per_kWh", "time_end"])    # Ta bort kolumner vi inte behöver
df = df.rename(columns={                                    # Ge kolumnerna kortare namn
    "SEK_per_kWh": "price_sek",
    "time_start": "start",
})

# --- 3. Gör om tiderna ---
df["start"] = pd.to_datetime(df["start"], utc=True)         # Gör om texten till riktiga tider
df["start"] = df["start"].dt.tz_convert("Europe/Stockholm") # Visa dem i svensk tid

# --- 4. Lägg till hjälpkolumner ---
df["date"] = df["start"].dt.date                            # Datumet, t.ex. 2026-01-01
df["hour"] = df["start"].dt.hour                            # Timmen, 0–23
df["minute"] = df["start"].dt.minute                        # Minuten: 0, 15, 30 eller 45
df["weekday"] = df["start"].dt.dayofweek + 1                # Veckodag: 1 = måndag, 7 = söndag
df["month"] = df["start"].dt.month                          # Månad: 1–12
df["is_weekend"] = df["weekday"] >= 6                       # True på lördag (6) och söndag (7)

# --- 5. Bestäm kolumnordningen ---
df = df[[
    "price_sek", "start", "area",                           # Värde, tid och plats
    "date", "hour", "minute",                               # Hjälpkolumner för dygnet
    "weekday", "month", "is_weekend",                       # Hjälpkolumner för vecka och år
]]

# --- 6. Kvalitetskontroll ---
# print(df.isna().sum())                                    # Antal tomma värden per kolumn (bör vara 0)
# print(df.duplicated(subset=["start", "area"]).sum())      # Antal dubbletter (bör vara 0)
# print(sorted(df["weekday"].unique()))                       # Se att dagarna faktiskt är 1 till 7

# --- 7. Titta på resultatet ---
print(df.head(5))                                          # Visa de första 5 raderna
