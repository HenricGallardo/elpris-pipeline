import pandas as pd                                         # Bibliotek för att arbeta med tabeller

df = pd.read_json("data/raw/prices.json")                   # Läs in rådatan som en tabell
df = df.drop(columns=["EXR", "EUR_per_kWh", "time_end"])    # Ta bort kolumner vi inte behöver

df = df.rename(columns={                                    # Ge kolumnerna kortare namn
    "SEK_per_kWh": "price_sek",
    "time_start": "start",
})
df["start"] = pd.to_datetime(df["start"], utc=True)         # Gör om texten till riktiga tider
df["start"] = df["start"].dt.tz_convert("Europe/Stockholm") # Visa dem i svensk tid
df["date"] = df["start"].dt.date                            # Datumet, t.ex. 2026-01-01
df["hour"] = df["start"].dt.hour                            # Timmen, 0–23
df["minute"] = df["start"].dt.minute                        # Minuten: 0, 15, 30 eller 45
df = df[["price_sek", "start", "area", "date", "hour", "minute"]]  # Lägg kolumnerna i den här ordningen

print(df.head(10))                                     # Visa de första 10 raderna