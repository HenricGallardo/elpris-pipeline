import requests                                  # Verktyg för att hämta data från internet
import time                                      # Verktyg för att kunna vänta/pausa
from datetime import date, timedelta             # Verktyg för att räkna med datum
import json                                      # Verktyg för att spara och läsa JSON-filer

start = date(2026, 1, 1)                         # Första dagen vi vill hämta: 1 januari 2026
end = date.today()                               # Dagens dag

all_data = []                        # En tom lista där vi samlar all data
day = start                          # Vi börjar på första dagen
price_class = ["SE1", "SE2", "SE3", "SE4"]  # Elområdena vi vill hämta (text, därför citattecken)

while day <= end:                    # Upprepa så länge dagen inte har passerat slutdatumet
    for area in price_class:         # För varje dag: gå igenom alla fyra elområden
        url = f"https://www.elprisetjustnu.se/api/v1/prices/{day:%Y}/{day:%m-%d}_{area}.json"
                                     # Bygg länken med datum OCH elområde, t.ex. .../2026/01-01_SE1.json
        response = requests.get(url) # Hämta datan från länken
        rows = response.json()       # Gör om svaret till en lista med rader

        for row in rows:             # Gå igenom varje rad för den här dagen och området
            row["area"] = area       # Lägg till vilket elområde raden gäller

        all_data.extend(rows)        # Lägg till raderna i vår stora lista
        print(day, area, "klar")     # Skriv ut vilken dag och vilket område som är hämtat
        time.sleep(0.2)              # Vänta 0,2 sekunder innan nästa hämtning

    day = day + timedelta(days=1)    # När alla fyra områden är klara: gå vidare till nästa dag

print(len(all_data))                 # Skriv ut hur många rader vi fick totalt
with open("data/raw/prices.json", "w") as f:   # Öppna (skapa) filen för att skriva ("w" = write)
    json.dump(all_data, f)                     # Skriv hela listan till filen

print("Sparat till data/raw/prices.json")      # Bekräfta att det gick