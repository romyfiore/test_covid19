
import json
from datetime import date
import requests
import sys
import pandas as pd

class ReadJsonFile():

    #TODO: DIVIDERE IL CODICE IN FUNZIONI

    def getDataFile(self):
        lst_DataCovid=[]
        lst_Region = []

        # file from github url
        url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'
        resp = requests.get(url)
        data = json.loads(resp.text)

        # Opening JSON file
        #with open("./file/dpc-covid19-ita-province.json", 'r') as file:

            # returns JSON object as
            # a dictionary
            #data = json.load(file)

        # Task 2 - Get Parameter Date
        if len(sys.argv)>=2:
            parameter_date = sys.argv[1]
            print(parameter_date)

            if parameter_date < '2020-02-24':
                print("Data precedente al 24 febbraio 2020, inserire una data successiva")
                return

            # TODO: CONTROLLARE IL FORMATO DELLA DATA

            date_now = parameter_date
        else:
            date_now = date.today()

        # Iterating through the json list
        for row in data:
            dict_DataCovid = {}
            if row['denominazione_regione'] != "":
                # get only value for today
                #if row['data'][:10] == date_now:
                if row['data'][:10] == '2023-05-03':
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

        #sorted from the region with the highest number of cases to the region with the smallest number of cases
        # (and in alphabetical order as secondary sorting)
        dict_value = sorted(dict_value.items(), key=lambda x: (-x[1], x[0]))
        print("List order value : ", dict_value)

        # Task 3 - Write Excel file
        columns = ['Region', 'Total Case']
        df = pd.DataFrame(dict_value, columns=columns)
        with pd.ExcelWriter('./pandas_to_excel.xlsx') as writer:
            df.to_excel(writer, sheet_name='sheet1')

oi = ReadJsonFile()
oi.getDataFile()