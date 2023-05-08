
import json
import urllib3
import orjson
from datetime import date

class ReadJsonFile():

    def getDataFile(self):
        lst_DataCovid=[]
        lst_Region = []

        #"https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-province.json"

        # Opening JSON file
        with open("./file/dpc-covid19-ita-province.json", 'r') as file:

            # returns JSON object as
            # a dictionary
            data = json.load(file)

            date_now= date.today()
            print(date_now)

            # Iterating through the json list
            for row in data:
                dict_DataCovid = {}
                if row['denominazione_regione'] != "":
                    # get only value for today
                    if row['data'][:10] == date_now:
                        dict_DataCovid['denominazione_regione'] = row['denominazione_regione']
                        dict_DataCovid['totale_casi'] = row['totale_casi']
                        lst_DataCovid.append(dict_DataCovid)
                        lst_Region.append(row['denominazione_regione'])

            # Distinct and sort lst_Region
            lst_Region = list(set(lst_Region))
            lst_Region.sort()

            # total of cases aggregated by Italian region
            dict_value = {}
            for region in lst_Region:
                total_case = 0
                for d in lst_DataCovid:
                    if 'denominazione_regione' in d and d['denominazione_regione'] == region:
                        total_case = total_case + d['totale_casi']
                dict_value[region] = total_case

            print("dict_value ----", dict_value)

            #sorted from the region with the highest number of cases to the region with the smallest number of cases
            # (and in alphabetical order as secondary sorting)
            dict_value = sorted(dict_value.items(), key=lambda x: (-x[1], x[0]))
            print(dict_value)
            # Closing file
            #f.close()

#
# Scrivere un software a riga di comando che legga i dati dal file JSON per provincia disponibile sul repository Github
# e stampi il totale complessivo dei casi
# (chiave "totali_casi" dell'oggetto relativo alla provincia) aggregati per regione italiana.
# I risultati devono essere ordinati dalla regione con il maggior numero di casi alla regione con il minor numero di casi
# (e in ordine alfabetico come ordinamento secondario).
# I dati da visualizzare devono essere relativi al giorno di esecuzione del software.
# Il file può essere recuperato da GitHub in fase di esecuzione o passato come opzione dalla riga di comando, come desideri.

oi = ReadJsonFile()
oi.getDataFile()