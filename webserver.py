
from datetime import date,datetime
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

BASE_URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

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

    def getResult(self, data, parameter_date):
        lst_DataCovid = []
        lst_Region = []

        # Get Parameter Date
        parameter_date = self.getPamaterDate()
        if parameter_date:
            print("Selected date: ", parameter_date)
        else:
            return

        # Iterating through the json list
        for row in data:
            dict_DataCovid = {}
            if row['denominazione_regione'] != "":

                # get correct format for date file
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
        return dict_value

    # method that responds to GET requests
    def do_GET(self):
        # Specifichiamo il codice di risposta
        self.send_response(200)
        # Specifichiamo uno o più header
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # message that will form the body of the response
        response = requests.get(f"{BASE_URL}")
        data = json.loads(response.text)

        #parameter date
        datenow = date.today()
        parameter_date = datenow.strftime('%d/%m/%Y')

        # execute code for result
        dict_value = self.getResult(data, parameter_date)
        if dict_value:
            message = "<h1>Lista Casi Totali per Regione nella data : " + parameter_date + "</h1>"
            message = message + "<table border='1px solid black'><tr><td>Regione</td><td>Casi</td></tr>"
            for value in dict_value:
                message = message + "<tr><td>" + value[0] + "</td><td>" + str(value[1]) + "</td></tr>"
            message = message + "</table>"
        else:
            message = "No values were found on the selected date: " + parameter_date
        self.wfile.write(message.encode("utf-8"))
        print("Open http://localhost:8000/ to see result.")
        return

    def run():
        print('Avvio del server...')
        # Specifichiamo le impostazioni del server
        # Scegliamo la porta 8081 (per la porta 80 sono necessari i permessi di root)
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('Server in esecuzione...')
        httpd.serve_forever()

testHTTPServer_RequestHandler.run()



