
from datetime import date,datetime
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from test_covid19.exercise import ReadJsonFile
from urllib.parse import parse_qs
from urllib.parse import urlparse

BASE_URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):


    def getPamaterDate(self):
        # Task 2 - Get Parameter Date
        parameter_date=""

        query_components = parse_qs(urlparse(self.path).query)
        if 'date' in query_components:
            parameter_date = query_components["date"][0]
            print(parameter_date)

        date_control = datetime.strptime('24/02/2020', '%d/%m/%Y')

        func = ReadJsonFile()
        if parameter_date:
            # Controllo il formato della data inserita
            value = func.date_validate(parameter_date)
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
        parameter_date = self.getPamaterDate()

        if parameter_date:
            print("Selected date: ", parameter_date)
        else:
            message = "Attention! The selected date not is in the format dd/mm/YYYY or the selected date is before to 24/02/2020"
            self.wfile.write(message.encode("utf-8"))
            return

        func = ReadJsonFile()

        # execute code for result
        dict_value = func.getResult(data, parameter_date)
        if dict_value:
            message = "<h1>Lista Casi Totali per Regione nella data : " + parameter_date + "</h1>"
            message = message + "<table border='1px solid black'><tr><td style='font-weight:bold'>Regione</td><td style='font-weight:bold'>Casi</td></tr>"
            for value in dict_value:
                message = message + "<tr><td>" + value[0] + "</td><td>" + str(value[1]) + "</td></tr>"
            message = message + "</table>"
        else:
            message = "No values were found on the selected date: " + parameter_date
        self.wfile.write(message.encode("utf-8"))
        return


    def run():
        print('Start server...')
        # server data
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('Server in execution...')
        print("Open http://localhost:8000?date=dd/mm/yyyy to see result.")
        httpd.serve_forever()

testHTTPServer_RequestHandler.run()



