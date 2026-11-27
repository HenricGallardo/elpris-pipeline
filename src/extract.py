import os                                        # Verktyg för att arbeta med mappar och filer
import requests                                  # Verktyg för att hämta data från internet
import time                                      # Verktyg för att kunna vänta/pausa
from datetime import date, timedelta             # Verktyg för att räkna med datum
import json                                      # Verktyg för att spara och läsa JSON-filer


def extract(start):                              # Tar emot startdatumet
    """Hämtar elpriser från start till i dag och sparar i data/raw/prices.json."""
    end = date.today()                           # Dagens dag

    all_data = []                                # En tom lista där vi samlar all data
    day = start                                  # Vi börjar på startdatumet som skickades in
    price_class = ["SE1", "SE2", "SE3", "SE4"]   # Elområdena vi vill hämta

    while day <= end:                            # Upprepa så länge dagen inte har passerat slutdatumet
        for area in price_class:                 # För varje dag: gå igenom alla fyra elområden
            url = f"https://www.elprisetjustnu.se/api/v1/prices/{day:%Y}/{day:%m-%d}_{area}.json"
            response = requests.get(url)         # Hämta datan från länken
            rows = response.json()               # Gör om svaret till en lista med rader

            for row in rows:                     # Gå igenom varje rad
                row["area"] = area               # Lägg till vilket elområde raden gäller

            all_data.extend(rows)                # Lägg till raderna i vår stora lista
            print(day, area, "klar")             # Visa vilken dag och vilket område som är hämtat
            time.sleep(0.2)                      # Vänta 0,2 sekunder innan nästa hämtning

        day = day + timedelta(days=1)            # Nästa dag

    print(len(all_data))                         # Hur många rader vi fick totalt
    os.makedirs("data/raw", exist_ok=True)      # Skapa mappen om den inte finns
    with open("data/raw/prices.json", "w") as f: # Öppna (skapa) filen för att skriva
        json.dump(all_data, f)                   # Skriv hela listan till filen

    print("Sparat till data/raw/prices.json")    # Bekräfta att det gick


if __name__ == "__main__":                       # Bara när filen körs direkt
    extract(date(2026, 1, 1))                    # Testa: hämta allt från 1 januari