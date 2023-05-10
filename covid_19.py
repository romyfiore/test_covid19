
import json
from datetime import date,datetime
import requests
import pandas as pd

class ReadJsonFile():

    def date_validate(self, date_text):
        format = "%d/%m/%Y"
        try:
            if bool(datetime.strptime(date_text, format)):
                res = True
            else:
                res = False
        except ValueError:
            res = False
        return res

    def getFile_to_url(self):
        # file from github url
        url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data

    def getPamaterDate(self):
        # Task 2 - Get Parameter Date
        parameter_date = input("Enter parameter date to 24/02/2020 (format dd/mm/yyyy): ")
        date_control = datetime.strptime('24/02/2020', '%d/%m/%Y')

        if parameter_date:
            # Controllo il formato della data inserita
            value = self.date_validate(parameter_date)
            if not value:
                print("Attention! The selected date not is in the format dd/mm/YYYY")
                return False
            else:
                if datetime.strptime(parameter_date, '%d/%m/%Y') < date_control:
                    print("Attention! The selected date is before to 24/02/2020.")
                    return False
        else:
            datenow = date.today()
            parameter_date = datenow.strftime('%d/%m/%Y')
        return parameter_date

    def changeFormatDate(self, date_file):
        date_file = datetime.strptime(date_file, '%Y-%m-%d')
        return date_file.strftime('%d/%m/%Y')

    def getCountTotalCaseForRegion(self, lst_Region, lst_DataCovid):
        dict_value = {}
        for region in lst_Region:
            total_case = 0
            for d in lst_DataCovid:
                if 'denominazione_regione' in d and d['denominazione_regione'] == region:
                    total_case = total_case + d['totale_casi']
            dict_value[region] = total_case
        return dict_value

    def createFileExcel(self, dict_value):
        try:
            columns = ['Region', 'Total Case']
            df = pd.DataFrame(dict_value, columns=columns)
            with pd.ExcelWriter('./Report_excel.xlsx') as writer:
                df.to_excel(writer, sheet_name='sheet1')
            print("Please control the file excel named Report_excel.xlsx.")
        except ValueError:
            print("File not created")

    def getDataFile(self):
        lst_DataCovid=[]
        lst_Region = []

        #Get Parameter Date
        parameter_date = self.getPamaterDate()
        if parameter_date:
            print("Selected date: ", parameter_date)
        else:
            return

        # Function return data file
        data = self.getFile_to_url()

        # Iterating through the json list
        for row in data:
            dict_DataCovid = {}
            if row['denominazione_regione'] != "":

                new_format_date_file = self.changeFormatDate(row['data'][:10])

                # get date for selected date
                if new_format_date_file == parameter_date:
                    dict_DataCovid['denominazione_regione'] = row['denominazione_regione']
                    dict_DataCovid['totale_casi'] = row['totale_casi']
                    lst_DataCovid.append(dict_DataCovid)
                    lst_Region.append(row['denominazione_regione'])

        # Distinct and sort lst_Region
        lst_Region = list(set(lst_Region))
        lst_Region.sort()

        # total of cases aggregated by Italian region
        dict_value = self.getCountTotalCaseForRegion(lst_Region, lst_DataCovid)

        # return the sorted list from the region with the highest number of cases to the region
        # with the smallest number of cases
        # (and in alphabetical order as secondary sorting)
        dict_value = sorted(dict_value.items(), key=lambda x: (-x[1], x[0]))
        if dict_value:
            print("List value at the date ", parameter_date, " is: ", dict_value)
        else:
            print("No values were found on the selected date: ", parameter_date)

        # Task 3 - Write Excel file
        self.createFileExcel(dict_value)

oi = ReadJsonFile()
oi.getDataFile()